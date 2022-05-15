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

Ms = [3];
dirs = {'/lowres_mach3','/mach3','/highres_mach3'};
colors = {[0 0.4470 0.7410],[0.9290 0.6940 0.1250],[0.8500 0.3250 0.0980],[0.4940 0.1840 0.5560]};

M = 3;

[xfinal,deflectionanglefinal] = tbm(M,gamma);
plot(deflectionanglefinal*(180/pi),xfinal*(180/pi),'k')

for i = 1:length(dirs)

    color = colors(i);
    color = color{1};

    dir = append(tbm_dir,dirs{i},'/thetabeta.csv');
    data = readtable(dir);
    theta = data{:,2};
    beta = data{:,3};
    plot(theta,beta,'o','MarkerEdgeColor',color)

end




set(0,'defaulttextinterpreter','latex')
set(gca, 'TickLabelInterpreter','latex')
% sgtitle('$\delta$-$\beta$-M Curve M=3.0')
xlabel('Deflection Angle $\theta$ (deg)')
ylabel('Shock Wave Angle $\beta$ (deg)')
legend('Anaylitcal, $M=3$', '24,000 Cells', '90,000 Cells', '360,000 Cells','location','northwest','interpreter','latex')
pos = get(h,'Position');
set(h,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
print(h,'-dpdf','-r0','figures/tbm_error.pdf')
