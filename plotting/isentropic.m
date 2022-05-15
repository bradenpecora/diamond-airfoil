function[T0r,P0r,rho0r] = isentropic(M,g)
    arguments
        M
        g = 1.4
    end
    T0r = 1 + (g-1)/2*M^2;
    P0r = T0r^(g/(g-1));
    rho0r = T0r^(1/(g-1));

end