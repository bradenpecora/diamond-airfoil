function [xfinal,deflectionanglefinal] = tbm(M1,gamma)


deflectionangle=(0:.01:20.2)*(pi/180);

% Equations
for i=1:length(deflectionangle)
    fun=@(x)((2*cot(x)*((M1^2*sin(x)^2-1)/(M1^2*(gamma+cos(2*x))+2))-tan(deflectionangle(i))));
    x(i)=fzero(fun,(20*pi/180));
end

deflectionangle1=(20.2:.01:33)*(pi/180);
for i=1:length(deflectionangle1)
    fun1=@(x)((2*cot(x)*((M1^2*sin(x)^2-1)/(M1^2*(gamma+cos(2*x))+2))-tan(deflectionangle1(i))));
    x1(i)=fzero(fun1,1);
end
deflectionanglefinal=[deflectionangle deflectionangle1];
xfinal=[x x1];
end

