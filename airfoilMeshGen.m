% Parameters
t = 0.1;            % Half thickness of airfoil at midway
c = 0.5;            % Half chord length
H = 4;              % Half height
Lw = 6;             % Length of wake region
Lf = 4;             % Length of fore region
d = .5;             % Width of "circular" region
fac = 1;            % Vertical stretch factor for d
type = "cylinder";   % Type of airfoil
n = 8;              % Number of points on airfoil and "circular" region 
ns = 1;             % Spline points
alpha = 10;         % Angle of attack
fileName = "blockMeshDict";

nx = [40,20,40,20,10,20];    % Radial, polar, east, north, west, south
ex = [2, 1, 2, 3, 5, 3];

% Requires n%8 = 0
n = n - mod(n,8);

% total number of vertices
N = 2*(2*n + n + 8);

% Total number of blocks
bN = 2*n + 4; 

Vert = zeros(3,N);          % x,y,z
Vert(3,1:N/2) = -0.05;
Vert(3,N/2+1:end) = 0.05;

% Creates airfoil and "circular" region vertices
for k = 1:2
    f = @(x)(airfoil(x,t + (k-1)*fac*d,c + (k-1)*d,type));  % Easy function call
    pL1 = pathLength(f,c + (k-1)*d,0,100);
    pL2 = pathLength(f,0,-c - (k-1)*d,100);
    set1 = (k-1)*n + [1, n/4+1, n/2+1];
    set2 = (k-1)*n + (1:(n/2+1));
    
    Vert(1:2,set1(1)) = [c + (k-1)*d;0];
    Vert(1:2,set1(2)) = [0;t + (k-1)*d*fac];
    Vert(1:2,set1(3)) = [-(c + (k-1)*d);0];
    
    for i = (setdiff(set2,set1) - (k-1)*n)
        if i < (n/4+1)
            g = @(x)(pathLength(f,c + (k-1)*d,x,100) - 4*(i-1)*pL1/n);
        else
            g = @(x)(pathLength(f,0,x,100) - 4*(i-n/4-1)*pL2/n);
        end
        opt = optimoptions('fsolve','Display','none');
        x = fsolve(g,(c+(k-1)*d)*cos(2*(i-1)*pi/n),opt);
        Vert(1:2,(k-1)*n + i) = [x;f(x)];
    end
    
    j = 1;
    for i = (n):-1:(n/2+2)
        Vert(1:2,(k-1)*n + i) = [1 0;0 -1]*Vert(1:2,(k-1)*n + 1+j);
        j = j + 1;
    end
end

% Creates outer vertices
m = N/2 - 2*n;
Vert(1:2,2*n + m/8+1) = [Lw,H];
Vert(1:2,2*n + 3*m/8+1) = [-Lf,H];

for i = (1:(m/8))
    Vert(1:2,2*n + i) = [Lw;Vert(2,n + i)];
end
for i = (m/8+2):(3*m/8)
    Vert(1:2,2*n + i) = [Vert(1,n + i - 2),H];
end
for i = (3*m/8+2):(m/2+1)
    Vert(1:2,2*n + i) = [-Lf,Vert(2,n + i - 4)];
end
j = 1;
for i = (m):-1:(m/2+2)
    Vert(1:2,2*n + i) = [1 0;0 -1]*Vert(1:2,2*n+1+j);
    j = j + 1;
end

% Flips vertices
for i = (N/2+1):N
    Vert(:,i) = [1 0 0; 0 1 0; 0 0 -1]*Vert(:,i-N/2);
end

Vert(1:2,1:2*n) = [cosd(alpha) sind(alpha); -sind(alpha) cosd(alpha)]*Vert(1:2,1:2*n);

% First n block in airfoil-circular region
Block = zeros(14,bN);
for i = 1:n
    s6 = mod(1+i,8);
    if s6 == 0
        s6 = n;
    end
    Block(1:4,i) = [i; n+i; n+s6; s6];
    Block(9:14,i) = [nx(1);nx(2);1;ex(1);ex(2);1];
end

% Outer blocks
for j = 1:4
    for i = (((-n/8 + 1):(n/8)) + 2*(j-1)*n/8)
        o = mod(i,n);
        if i < 1
            num = bN - i;
        else
            num = n + o + j - 1;
        end
        if o == 0
            o = n;
        end

        s2 = (17/8 - 2*(j-1)/8)*n + m*mod(-1 + 2*(j-1),8)/8 + 1 + i;
        if s2 > N/2
            s2 = 2*n + mod(s2,N/2);
            s22 = s2+1;
        elseif s2 == N/2
            s22 = 2*n + mod(s2+1,N/2);
        else 
            s22 = s2+1;
        end

        if o == (n-1)
            s5 = n;
        else 
            s5 = mod(o+1,n);
        end

        Block(1:4,num) = [n+o; s2; s22; n+s5];
        Block(9:14,num) = [nx(2+j);nx(2);1;ex(2+j);ex(2);1];
    end
    s3 = (9+2*(j-1))/8;
    s4 = 2*n + (1 + 2*(j-1))*m/8;
    Block(1:4,s3*n + j) = [s3*n+1; s4; s4+1; s4+2];

    s7 = mod(j,4);
    if s7 == 0
        s7 = 4;
    end
    Block(9:14,s3*n+j) = [nx(2+s7);nx(2+mod(j,4)+1);1;ex(2+s7);ex(2+mod(j,4)+1);1];
end
Block(5:8,:) = Block(1:4,:) + N/2;
Block(1:8,:) = Block(1:8,:) - 1;



fileStr = [ append("// nx = [ ", num2str(nx(1))," ", num2str(nx(2))," ", num2str(nx(3))," ",...
            num2str(nx(4))," ", num2str(nx(5))," ", num2str(nx(6)), " ]"), ...
            append("// ex = [ ", num2str(ex(1))," ", num2str(ex(2))," ", num2str(ex(3))," ",...
            num2str(ex(4))," ", num2str(ex(5))," ", num2str(ex(6)), " ]"), ...
            append("// c = ", num2str(c)),...
            append("// t = ", num2str(t)),...
            append("// d = ", num2str(t)),...
            append("// fac = ", num2str(fac)),...
            append("// H = ", num2str(H)),...
            append("// Lf = ", num2str(Lf)),...
            append("// Lw = ", num2str(Lw)),...
            append("// n = ", num2str(8)),...
            append("// Airfoil type is ", type),...
            " " ,...
            "FoamFile" , ...
            "{", ...
            "version 2.0;",...
            "format ascii;",...
            "class dictionary;",...
            "object blockMeshDict;",...
            "}",...
            " ",...
            "convertToMeter = 1.0;",...
            " ",...
            "vertices",...
            "("];

for i = 1:length(Vert(1,:))
    fileStr = [fileStr, append("     ( ", num2str(Vert(1,i)), ...
        " ", num2str(Vert(2,i))," ", num2str(Vert(3,i)), " ) //", num2str(i-1))];
end
fileStr = [fileStr, ");", " ", "blocks", "("];

for i = 1:length(Block(1,:))
    fileStr = [fileStr, append("     //block ",num2str(i-1)),...
        append("     hex (", num2str(Block(1,i)), " ", num2str(Block(2,i)), " ",...
        num2str(Block(3,i)), " ", num2str(Block(4,i)), " ", num2str(Block(5,i)), " ", ...
        num2str(Block(6,i)), " ", num2str(Block(7,i)), " ", num2str(Block(8,i)), ") ( ",...
        num2str(Block(9,i)), " ", num2str(Block(10,i)), " ", num2str(Block(11,i)), ...
        ") simpleGrading ( ", num2str(Block(12,i)), " ", num2str(Block(13,i)), " ", ...
        num2str(Block(14,i)), ")")];
end


% CHANGE TO SPLINES
if type ~= "diamond"
    fileStr = [fileStr, ");", " ", "edges", "("];
    
    f1 = @(x)(airfoil(x,t,c,type));
    f2 = @(x)(airfoil(x,t + fac*d,c + d,type)); 
    
    for i = 1:(n/2)
        x1 = midpoint(f1,Vert(1,i),Vert(1,mod(i,n)+1),ns);
        x2 = midpoint(f2,Vert(1,i+n),Vert(1,mod(i,n)+1+n),ns);
        fileStr = [fileStr, append("     arc ", num2str(i-1), " ", num2str(mod(i,n)), ...
            " ( ", num2str(x1), " ", num2str(f1(x1)), " -0.05 )"), ...
            append("     arc ", num2str(i-1+n), " ", num2str(mod(i,n)+n), ...
            " ( ", num2str(x2), " ", num2str(f2(x2)), " -0.05 )"), ...
            append("     arc ", num2str(i-1+N/2), " ", num2str(mod(i,n)+N/2), ...
            " ( ", num2str(x1), " ", num2str(f1(x1)), " 0.05 )"), ...
            append("     arc ", num2str(i-1+n+N/2), " ", num2str(mod(i,n)+n+N/2), ...
            " ( ", num2str(x2), " ", num2str(f2(x2)), " 0.05 )")];
    end
    for i = (n/2+1):n
        x1 = midpoint(f1,Vert(1,i),Vert(1,mod(i,n)+1),ns);
        x2 = midpoint(f2,Vert(1,i+n),Vert(1,mod(i,n)+1+n),ns);
        fileStr = [fileStr, append("     arc ", num2str(i-1), " ", num2str(mod(i,n)), ...
            " ( ", num2str(x1), " ", num2str(-f1(x1)), " -0.05 )"), ...
            append("     arc ", num2str(i-1+n), " ", num2str(mod(i,n)+n), ...
            " ( ", num2str(x2), " ", num2str(-f2(x2)), " -0.05 )"), ...
            append("     arc ", num2str(i-1+N/2), " ", num2str(mod(i,n)+N/2), ...
            " ( ", num2str(x1), " ", num2str(-f1(x1)), " 0.05 )"), ...
            append("     arc ", num2str(i-1+n+N/2), " ", num2str(mod(i,n)+n+N/2), ...
            " ( ", num2str(x2), " ", num2str(-f2(x2)), " 0.05 )")];
    end
end

fileStr = [fileStr, " ", ");", " ",...
           "boundary",...
           "( ",...
           "   inlet",...
           "   {",...
           "      type patch;",...
           "      faces",...
           "      (",...
           "         (22 54 55 23)",...
           "         (23 55 56 24)",...
           "         (24 56 57 25)",...
           "         (25 57 58 26)",...
           "       );",...
           "   }",...
           "   outlet",...
           "   {",...
           "      type patch;",...
           "      faces",...
           "      (",...
           "         (18 50 49 17)",...
           "         (17 49 48 16)",...
           "         (16 48 63 31)",...
           "         (31 63 62 30)",...
           "       );",...
           "   }",...
           "   airfoil",...
           "   {",...
           "      type wall;",...
           "      faces",...
           "      (",...
           "         (0 32 33 1)",...
           "         (1 33 34 2)",...
           "         (2 34 35 3)",...
           "         (3 35 36 4)",...
           "         (4 36 37 5)",...
           "         (5 37 38 6)",...
           "         (6 38 39 7)",...
           "         (7 39 32 0)",...
           "       );",...
           "   }",...
           "   top",...
           "   {",...
           "      type symmetryPlane;",...
           "      faces",...
           "      (",...
           "         (22 54 53 21)",...
           "         (21 53 52 20)",...
           "         (20 52 51 19)",...
           "         (19 51 50 18)",...
           "       );",...
           "   }",...
           "   bottom",...
           "   {",...
           "      type symmetryPlane;",...
           "      faces",...
           "      (",...
           "         (26 58 59 27)",...
           "         (27 59 60 28)",...
           "         (28 60 61 29)",...
           "         (29 61 62 30)",...
           "       );",...
           "   }",...
           ");"];

fid = fopen(fileName,'w');
fprintf(fid,'%s\n',fileStr(:));
fclose(fid);
% writelines(fileStr,fileName)
clear opt x g theta set* pL* m s* num i j k o ns f


%% Plotting
display = 1;
if display == 1
    hold on;
    plot([Vert(1,1:n), Vert(1,1)],[Vert(2,1:n), Vert(2,1)])
    plot([Vert(1,(n+1:2*n)), Vert(1,n+1)],[Vert(2,(n+1:2*n)), Vert(2,n+1)])
    axis([-(Lf+1),(Lw+1),-(H+1),(H+1)])
end

%%
f = @(x)(airfoil(x,.1,.5,"biconvex"));
x = -.5:.001:.5;
y = zeros(1,length(x));
for i = 1:length(x)
    y(i) = f(x(i));
end

plot(x,y,x,-y)
axis([-1 1 -1 1])
%% Functions
function y = airfoil(x,t,c,type)
    % parametric representation of the airfoil
    arguments
        x
        t = 1
        c = t
        type = "cylinder"
    end
    switch type
        case "cylinder"
            y = t*sqrt(1-x.^2/c^2);
        case "diamond"
            y = t*(1-abs(x/c));
        case "biconvex"
            if abs(x) < 19*c/20
                y = t*sqrt(1-x.^2/(c)^2);
            else
                yi = t*sqrt(1-(19*c/20).^2/(c)^2); 
                y = yi - 20*yi*(abs(x) - 19*c/20)/c;
            end
        case "airfoil"
            if (x > -c/2) && (x < c/2) 
                y = t*sqrt(1-(x+c/2).^2/(3*c/2)^2);
            elseif x >= c/2
                yi = t*sqrt(1-(c).^2/(3*c/2)^2);
                y = yi - yi*2/c*(x-c/2);
            else
                y = t*sqrt(1-(x+c/2).^2/(c/2)^2);
            end
    end

end

function L = pathLength(fun,xi,xf,n)
    x = linspace(xi,xf,n);
    L = 0;
    dx = x(2)-x(1);
    for i = 1:(length(x)-1)
        dfun = (fun(x(i+1))-fun(x(i)));
        L = L + sqrt(dx^2+dfun^2);
    end
    L = abs(L);
end

function x = midpoint(fun,x1,x2,ns)
    pL1 = pathLength(fun,0,x1,100);
    pL2 = pathLength(fun,0,x2,100);
    pL = (pL1+pL2)/2;

    x = zeros(1,ns);
    for i = 1:ns
        g = @(x)(pathLength(fun,0,x,100) - i*pL/ns);
        opt = optimoptions('fsolve','Display','none');
        xi = fsolve(g,(x1+x2)/2,opt);
        x(i) = xi;
    end
end