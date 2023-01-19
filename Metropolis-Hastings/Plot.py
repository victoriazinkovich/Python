def f_plot(*args, **kwargs):
    xlist = []
    ylist = []
    for i, arg in enumerate(args):
        if(i % 2 == 0):
            xlist.append(arg)
        else:
            ylist.append(arg) 
    
    colors = kwargs.pop('colors', 'k')
    linewidth = kwargs.pop('linewidth', 1.)
    labels = kwargs.pop('labels', 'k')
    
    fig = plt.figure()
    fig.set_size_inches(10, 5)
    ax = fig.add_subplot(111)
    i = 0
    for x, y, color, label in zip(xlist, ylist, colors, labels):
        i += 1
        ax.plot(x, y, color=color, linewidth=linewidth, label=label)
    
    ax.set_xlabel(u'Temperature, K', size=12)
    ax.set_ylabel(u'Average Energy', size=12)
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    
    ax.minorticks_on()
    ax.grid(which='major', color = 'lightgray')
    ax.grid(which='minor', color = 'lightgray', linestyle = ':')
    ax.legend()

colors = ['#6666FF', '#B552AD']
labels = ['Modelling', 'Experimental']


# Looking at the variances
temps1 = [1.7, 2, 2.5, 3, 4, 7]
colors = ['#FF7889', '#8A5082', '#6F5F90', '#758EB7', '#A5CAD2', '#E8B7D4']

fig, ax = plt.subplots(figsize=(10,6))
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
ax.set_xlabel(u'Energies distribution', size=12)
ax.set_ylabel(u'Density', size=12)
    
for T, color in zip(temps1, colors):
    chain = make_chain(n, m)
    energies = metropolis(chain, T, etol=1e-6)
    average = sum(energies) / len(energies)
    sns.distplot(energies, hist=True, kde=True, hist_kws={'edgecolor':'black'}, kde_kws={'linewidth':2}, bins=10, color=color)
    disp = 0
    for i in range(len(energies)):
        disp += (energies[i] - average)**2
    disp = math.sqrt(disp/len(energies))
    print("Дисперсия: ", round(disp, 1))
    print("done: T =", T)
