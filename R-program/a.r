library("fda")
basis13 = create.bspline.basis(c(0,10), 13)
tvec = seq(0,1,len=13)
sinecoef = sin(2*pi*tvec)
sinefd = fd(sinecoef, basis13, list("t","","f(t)"))
op = par(cex=1)
plot(sinefd, lwd=2)
points(tvec*10, sinecoef,lwd=10)    #lwd is brightness of point
par(op)
