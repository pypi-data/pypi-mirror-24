#-------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2014 Luzzi Valerio for Gecosistema S.r.l.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Name:
# Purpose:    Kriging on Quality
#
# Author:      Luzzi Valerio
#
# Created:     20/03/2014
#-------------------------------------------------------------------------------

#SRS =  "+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=500092 +y_0=-3999800 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
#
#Default SRS= epsg:3857 if not defined in shape
SRS = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"
#------------------------------------------------------------------------------
#	string functions
#------------------------------------------------------------------------------
len<-function(arr)length(arr)
contains<-function(text,search){return(length(grep(search,text))>0)}
alltrim <- function (text) gsub("^\\s+|\\s+$", "",text)
upper<-function(text)toupper(text)
lower<-function(text)tolower(text)
left<-function(text,n)substr(text,1,n)
juststem<-function(text) sub("^([^.]*).*", "\\1", basename(text)) 
#juststem<-function(text)file_path_sans_ext(basename(text))
justpath<-function(text)dirname(text)
justext<-function(text) substr(text,nchar(text)-2,nchar(text))
forceext<-function(text,ext) sub("^([^.]*).*", paste("\\1",ext,sep="."), text) 
#forceext<-function(text,ext) paste(file_path_sans_ext(text),ext,sep=".")
mkdirs<-function(text)dir.create(text,recursive=TRUE,showWarnings = FALSE)
isDate<-function(text){res = tryCatch(length(as.Date(text))>0,error=function(e){return(FALSE)});return(res)}
logger<-function(text){f=file("log.txt",open="at");writeLines(text,f);print(text);close(f);}
progression<-function(text,perc){f=file("interp.progress",open="at");writeLines(text,f);print(text);close(f);}



#------------------------------------------------------------------------------
#	CreateMask
#------------------------------------------------------------------------------
CreateMask<-function(piezo,Buffer=200,pixelsize=10){

	bbox = bbox(piezo)
	minx = bbox[1]-Buffer
	miny = bbox[2]-Buffer
	maxx = bbox[3]+Buffer
	maxy = bbox[4]+Buffer
	x= seq(minx,maxx,pixelsize)
	y= seq(miny,maxy,pixelsize)
	
	grid = expand.grid(X=x,Y=y)
	grid$Z = 0.0
	gridded(grid)=~X+Y
	proj4string(grid)=proj4string(piezo)
	#writeGDAL(grid["Z"],"buffer.tif")
	return(grid)
}

#------------------------------------------------------------------------------
#	DetectFormulaUK -  Formula for universal Kriging
#------------------------------------------------------------------------------
DetectFormulaUK <- function( prec ){

	#Creo la formula per l'Universal Kriging
	#Cerco il nome della variabile dipendente
	VALUE = "VALUE"
	cn  = names( prec )  #Nomi dei campi 
	candidates = c("VALUE","value")
	for(varname in candidates){
		if ( isTRUE(grep(varname,cn)) ){
			VALUE = varname
			break
		}
	}
	
	#Creo la formula per l'Universal Kriging
	cn = cn[cn!=VALUE] #Rimuovo "VALUE" non deve comparire a dx nella formula
	f = paste(cn,collapse="+")
	f = paste(VALUE,"~",f)
	f = as.formula(f)
	return(f)
}


#------------------------------------------------------------------------------
#	OrdinaryKriging | IDW
#------------------------------------------------------------------------------
Interpolation <-function( prec ,buffer=200,pixelsize=10, filename="out.tif", type ="AUTO", sformula="", RemoveNegativeValues=FALSE)
{
	dem <- CreateMask(prec,buffer,pixelsize)
	xy  <- as.data.frame(coordinates(dem))
	dem@data$x<-xy$X
	dem@data$y<-xy$Y

	#Rinomino la banda1 in z 
	colnames(dem@data)[1]="z"
	
	#Remove na from prec
	prec<-prec[!is.na(prec$VALUE),]

	#Overlay prendo il valori nei punti delle stazioni
	ov<-over(prec,dem)
	prec$x <- ov$x
	prec$y <- ov$y
	prec$z <- ov$z	
	
	
	#print(prec)
	
	#Automap
	if (type == "AUTO"){
		prec_ok <-autoKrige(VALUE~1,prec,dem)
		prec_ok = prec_ok$krige_output		
		prediction = prec_ok[1]
	}	
	#Universal Kriging
	if (type == "UK-AUTO"){
		if (sformula!="--") fm = as.formula(sformula) else fm = DetectFormulaUK(prec@data)
		print(fm)
		prec_ok <-autoKrige(fm,prec,dem)
		prec_ok = prec_ok$krige_output	
		#print(head(prec_ok[1]@data))
		prediction = prec_ok[1]
	}		
	if (type =="UK"){
		# trend model 
		if (sformula!="--") fm = as.formula(sformula) else fm = DetectFormulaUK(prec@data)
		lm.prec <- lm(fm, prec)
		fm <-step(lm.prec)
		residui = residuals(fm)

		null.vgm <- vgm(var(residui), "Sph", sqrt(areaSpatialGrid(dem))/4, nugget=0) # initial parameters
		vgm_r    <- fit.variogram(variogram(residui~1, prec) ,model=null.vgm)
		prec_ok <-  krige(as.formula(fm), locations=prec, newdata=dem, model=vgm_r) 
		prediction = prec_ok[1]
	
	}
	#Ordinary Kriging
	if ( type =="OK"){
		null.vgm <- vgm(var(prec$VALUE), "Sph", sqrt(areaSpatialGrid(dem))/4, nugget=0)
		vgm_v<- fit.variogram(variogram(prec$VALUE~1, prec), model=null.vgm)
		#prec_ok <- krige(VALUE~1, locations=prec, newdata=dem, model=vgm_v,maxdist=2000)
		prec_ok <- krige(VALUE~1, locations=prec, newdata=dem, model=vgm_v)
		prediction = prec_ok[1]
	}
	#Inverse Distance
	if( type =="IDW"){
		prec_ok <- idw(VALUE~1, prec, dem,idp=1.0,nmax=10,maxdist=450)
		prediction = prec_ok[1]
	}
	#Inverse Distance
	if( type =="IDW2"){
	  prec_ok <- idw(VALUE~1, prec, dem,idp=2.0,maxdist=Inf)
	  prediction = prec_ok[1]
	}
	mkdirs(justpath(filename))
	
	#Remove negative values!!!!
	if (RemoveNegativeValues){
		prediction@data[prediction@data<0]=0}
	
	writeGDAL(prediction,filename)	
	return(prec_ok)
}



#------------------------------------------------------------------------------
#	QueryKriging
#------------------------------------------------------------------------------
QueryKriging<-function(fileshp,filename="QueryKriging.tif",buffer=200,pixelsize=10,type="OK",sformula="",RemoveNegativeValues=FALSE){
	
	piezo=c()

	if (justext(tolower(alltrim(fileshp)))=="shp"){
		piezo = readOGR(fileshp,juststem(fileshp))
		if (is.na(proj4string(piezo)))
			proj4string(piezo) = CRS(SRS)
	}
	if (length(piezo)>0){
		print(paste("Number of points to krige",length(piezo)))
		#writeOGR(piezo,"prec.shp","prec","ESRI Shapefile")
		Interpolation(piezo,buffer,pixelsize,filename,type,sformula,RemoveNegativeValues)
		return(filename)
	}
	return(FALSE)
}


#------------------------------------------------------------------------------
#	Main
#------------------------------------------------------------------------------
Main <- function(){
  #Suppress Warning
  options(warn=-1)

	#Getting command arguments
	args <- commandArgs(trailingOnly = TRUE)
	res = FALSE

	
	#load required libraries
	library(sp)
	library(rgdal)
	library(gstat)
	library(automap)
	library(tools)
	
	
	#Test
	if (length(args)==0){
		
		setwd("D:\\Program Files (x86)\\SICURA\\apps\\awesome\\data\\SIMS\\2016-11-05 14-57")
		fileshp		= "conc.shp"
		filename  = forceext(fileshp,"tif")
	
		#method = "UK-AUTO" 
		method = "AUTO" 
		sformula="--" 
		pixelsize=500
		RemoveNegativeValues=FALSE
		res = QueryKriging(fileshp,filename,200,pixelsize,method,sformula,RemoveNegativeValues)

		return(res)
	}
	if (length(args)>=5){
		
		fileshp		  = args[1]
		method		  = args[2]  #AUTO|UK|UK-AutoKrige|OK|IDW
		pixelsize   = as.numeric(args[3])
		sformula    = args[4]
		RemoveNegativeValues = as.logical(args[5]) #remove non-sense negative values caused by interpolation 

		filename    = if (length(args[6])>0) args[6] else forceext(fileshp,"tif")
		
		#print(fileshp)
		#print(method)
		#print(pixelsize)
		#print(sformula)
		#print(RemoveNegativeValues)
		#print(args[6])
		#print(filename)
		#comment next 2 lines
		# ...
		#pixelsize	=50	 
		#Pay attention here!!
		res = QueryKriging(fileshp,filename,200,pixelsize,method,sformula,RemoveNegativeValues)

		return(res)
	}
	return(res)
}

#------------------------------------------------------------------------------
#	Main-loop launch
#------------------------------------------------------------------------------
libray = "D:\\Program Files (x86)\\SICURA\\apps\\common\\bin\\R\\R-3.3.2\\library"
##install.packages("sp",     lib=libray)
##install.packages("rgdal",  lib=libray)
##install.packages("gstat",  lib=libray)
##install.packages("automap",  lib=libray)
##install.packages("tools",  lib=libray)
print(Main())




