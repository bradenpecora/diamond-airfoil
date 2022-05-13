% run from parent directory
clear all
close all
clc
fig = 0;

fig = fig+1;
h = figure(fig);
set(h,'Units','Inches');
hold on

gamma = 1.4;

tbm_dir = 'simulations/theta-beta-m';

Ms = [2];
colors = {[0 0.4470 0.7410],[0.9290 0.6940 0.1250],[0.8500 0.3250 0.0980],[0.4940 0.1840 0.5560]};


for i = 1:length(Ms)
    M = Ms(i);
    color = colors(i);
    color = color{1};
    [xfinal,deflectionanglefinal] = tbm(M,gamma);
    plot(deflectionanglefinal*(180/pi),xfinal*(180/pi),'color',color)

    dir = append(tbm_dir,'/mach',num2str(M),'/thetabeta.csv');
    data = readtable(dir);
    theta = data{:,2};
    beta = data{:,3};
    plot(theta,beta,'s','MarkerFaceColor',color,'MarkerEdgeColor','k')

end




set(0,'defaulttextinterpreter','latex')
set(gca, 'TickLabelInterpreter','latex')
% sgtitle('$\delta$-$\beta$-M Curve M=3.0')
xlabel('Deflection Angle $\delta$ (deg)')
ylabel('Shock Wave Angle $\beta$ (deg)')
legend('Mach 3 - Anaylitcal', 'Mach 3 - Numerical', 'Mach 4 - Analytical', 'Mach 4 - Numerical', 'Mach 5 - Analytical', 'Mach 5 - Numerical', 'location','best','interpreter','latex')
pos = get(h,'Position');
set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% print(h,'-dpdf','-r0','figures/tbm.pdf')
