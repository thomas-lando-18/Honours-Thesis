function sys = system_constants()
    % This function will be upgraded to perform actual calculationn based
    % on an input geometry however for the current form, it will use the
    % parameters given in P.Yang's Conference Paper
    
    ft2m = 0.3048;
    
    sys.m = 5.12;
    sys.c = 0.5;
    sys.alt = 30e3*ft2m;
    sys.a = -0.5;
    sys.I_a = 0.0031;
    sys.I_b = 0.000021;
    sys.b = 0.799;
    
    sys.s_a = 0.0309;
    sys.s_b = 0.00086;
    
    sys.c_a = 3.12;
    sys.c_b = 357.1^2;
    sys.c_h = 2542;
    
    sys.M = 3;
    
    [sys.rho, sys.u] = GetAtmosVal(sys.alt, sys.M);
    sys.omega_ac = 357.1;
    sys.k = sys.omega_ac/sys.u;
    
    sys.T = Tconstants(sys.a, sys.c);
    sys.C = CkCalculation(sys.k);
    
end