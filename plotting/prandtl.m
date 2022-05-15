function M2 = prandtl(M1,turn)
    nu = sqrt(2.4/.4) * atand(sqrt(.4/2.4*(M1^2-1)))-atand(sqrt(M1^2-1));
    nu = nu + turn;
    syms M
    S = vpasolve(sqrt(2.4/.4) * atand(sqrt(.4/2.4*(M^2-1)))-atand(sqrt(M^2-1))-nu,M,0.1);
    clear M
    M2 = double(S);
    clear S
end