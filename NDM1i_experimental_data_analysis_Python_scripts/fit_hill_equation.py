import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
 
# Read binding data:
def load_binding_data( filename ):
    concentrations = []
    activities = []
    activity_error = []
    n = -100
    y0 = -100
    yinf = -100
    IC50 = -100
    nerr = -100
    y0err = -100
    yinferr = -100
    IC50err = -100
    headerconc=-100
    headeravg=-100
    headererr=-100
    if filename != "xxx":
        with open(filename) as curfile:
            lines = curfile.readlines()
        print( "Read " + filename )
        indata=False
        finisheddata=False
        for line in lines:
            if finisheddata == False:
                if indata == False :
                    #Assume first line is header.
                    indata = True
                    linesplit = line.split()
                    for i in range(len(linesplit)) :
                        if linesplit[i].startswith("[") :
                            headerconc = i
                        elif linesplit[i].startswith("Avg"):
                            headeravg = i
                        elif linesplit[i].startswith("StdErr") :
                            headererr = i
                    assert headerconc != -100
                    assert headeravg != -100
                    continue
                else:
                    linesplit = line.split()
                    if( len(linesplit) == 0 ) :
                        indata = False
                        finisheddata = True
                        continue
                    assert len(linesplit) > headerconc, "Could not parse \"" + line + "\". headerconc=" + str(headerconc)
                    assert len(linesplit) > headeravg, "Could not parse \"" + line + "\".  headeravg=" + str(headeravg)
                    if headererr != -100 :
                        assert len(linesplit) > headererr, "Could not parse \"" + line + "\". headererr=" + str(headererr)
                    concentrations.append( float(linesplit[headerconc]) )
                    activities.append( float(linesplit[headeravg]) )
                    if headererr != -100 :
                        activity_error.append( float(linesplit[headererr]) )
            else:
                linesplit = line.split()
                if len(linesplit) == 3:
                    if( linesplit[0] == "n" ):
                        n = int(linesplit[1])
                        nerr = float( linesplit [2] )
                    elif( linesplit[0] == "y0"):
                        y0 = float(linesplit[1])
                        y0err = float(linesplit[2])
                    elif( linesplit[0] == "yinf"):
                        yinf = float(linesplit[1])
                        yinferr = float(linesplit[2])
                    elif( linesplit[0] == "IC50"):
                        IC50 = float(linesplit[1])
                        IC50err = float(linesplit[2])
 
    return ( concentrations, activities, activity_error, (n, nerr), (y0, y0err), (yinf, yinferr), (IC50, IC50err) )
 
# Assert that we've been passed four argument: a datafile to fit:
assert len( sys.argv ) == 5, "Expected four arguments: a file to fit to the Hill equation, an estimated y0, an estimated yinf, and an estimated IC50."
 
# Read the data:
binding_data = load_binding_data( sys.argv[1] )

# Ensure some tiny uncertainty in all points to avoid divide-by-zero errors during fitting:
for i in range( len( binding_data[2] ) ) :
    if binding_data[2][i] < 0.001 :
        binding_data[2][i] = 0.01
 
# Function to fit:
hilleq = lambda x, y0, yinf, IC50 : ( y0 - yinf ) / ( 1 + (IC50/ x ) ) + yinf
 
# Perform the fitting:
IC50 = float( sys.argv[4] )
IC50err = 0
y0 = float( sys.argv[2] )
y0err = 0
yinf = float( sys.argv[3] )
yinferr = 0
n = 1
nerr = 0
 
x_data = np.array( binding_data[0] )
y_data = np.array( binding_data[1] )
y_err = np.array( binding_data[2] )
print( x_data )
print( y_data )
print( y_err )
 
best_fit_vals, covar = curve_fit(hilleq, x_data, y_data, p0=[y0,yinf,IC50], sigma=y_err, absolute_sigma=True )
print( "best_fit_vals:", best_fit_vals )
assert( len(best_fit_vals) == 3)
y0 = best_fit_vals[0]
yinf = best_fit_vals[1]
IC50 = best_fit_vals[2]
 
# Getting fit errors.
uncertainty_vals = np.sqrt(np.diagonal(covar))
print( "uncertainty_vals:", uncertainty_vals )
assert( len(uncertainty_vals) == 3 )
y0err = uncertainty_vals[0]
yinferr = uncertainty_vals[1]
IC50err = uncertainty_vals[2]
 
print( "n\t" + str(n) + "\t" + str(nerr) )
print( "y0\t" + str(y0) + "\t" + str(y0err) )
print( "yinf\t" + str(yinf) + "\t" + str(yinferr) )
print( "IC50\t" + str(IC50) + "\t" + str(IC50err) )
 
# Plot the data and the fit:
fig, ax = plt.subplots( nrows=1, ncols=1 )
plotmarker = matplotlib.markers.MarkerStyle( marker="o", fillstyle="full" )
 
ax.set_xlabel( "[peptide] (μM)" )
ax.set_ylabel( "Normalized activity" )
sc = ax.scatter( binding_data[0], binding_data[1], marker=plotmarker, edgecolors="none", s=10, c='b' )
eb = ax.errorbar( binding_data[0], binding_data[1], yerr=binding_data[2], linestyle="None", elinewidth=0.5  )
#Construct the best fit curve
xprime = []
interpolation_points = 50
for j in range(len(binding_data[0]) - 1) :
    for k in range(interpolation_points) :
        xprime.append( float(k)/float(interpolation_points) * ( binding_data[0][j+1] - binding_data[0][j] ) + binding_data[0][j] )
xprime.append( binding_data[0][len(binding_data[0])-1] )
yprime = []
for x in xprime :
    if( x == 0  ) :
        yprime.append( yinf )
    else :
        yprime.append( (y0-yinf)/( 1 + (IC50/x)**n ) + yinf )
ax.plot( xprime, yprime, 'r-', linewidth=0.5 )
 
# Calculate and plot residuals:
resids = [ yinf - binding_data[1][0] ]
for j in range(1, len(binding_data[0]) ) :
    resids.append( -((y0-yinf)/( 1 + (IC50/ binding_data[0][j] )**n ) + yinf) + binding_data[1][j] )
ax2 = inset_axes( ax, width="40%", height="25%", loc=1 )
insetplot = ax2.scatter( binding_data[0], resids, marker=plotmarker, edgecolors="none", s=2.0, c='b' )
ebinsert = ax2.errorbar( binding_data[0], resids, yerr=binding_data[2], linestyle="None", elinewidth=0.5, c='b' )
ax2.set_ylim( -0.1, 0.1 )
ax2.axhline(0, c='red', linewidth=0.5)
 
plt.show()
