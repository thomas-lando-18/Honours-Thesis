function Matrices = StateSpaceBuild(sys)
    % EOM
    Matrices.A = [sys.I_a, sys.I_b+sys.b*(sys.c-sys.a)*sys.s_b, sys.s_a;
                sys.I_b+sys.b*(sys.c-sys.a)*sys.s_b, sys.I_b, sys.s_b;
                sys.s_a, 0,sys.m];
            
    Matrices.B = zeros(3,3);
    
    Matrices.C = [sys.c_a,0,0;
                  0,sys.c_b,0;
                  0,0,sys.c_h];
              
    % Force/Moment Values
    rho = sys.rho;
    a = sys.a;
    b = sys.b;
    T = sys.T;
    c = sys.c;
    v = sys.u;
    C_k = sys.C(1);
    
    Matrices.D = [-rho*b^4*pi*(1/8+a^2), rho*b^4*(T{7}+(c-a)*T{1}),...
        rho*a*b^3*pi;
        -2*rho*b^4*T{13}, rho*b^4*T{3}*1/pi, -rho*b^3*T{1};
        -rho*b^3*a*pi, rho*b^3*T{1},0];
    
    Matrices.E = [-rho*b^3*pi*v(0.5-a)-2*rho*v*b^2*pi*C_k*(a^2-0.25),...
        -rho*b^3*v*(T{1}-T{8}-(c-a)*T{4}+0.5*T{11})+rho*b^3*v*T{11}*(a+0.5)*C_k,...
        2*rho*v*b^2*pi*(a+0.5)*C_k;
        -rho*v*b^3*(-2*T{9}-T{1}+T{4}*(a+0.5))-rho*v*b^3*T{12}*C_k(1/2-a),...
        rho*b^3*v*T{4}*T{11}/(2*pi)-rho*v*b^3*T{11}*T{12}*C_k/(2*pi),...
        -rho*v*b^2*T{12}*C_k;
        -rho*b^2*v*pi+2*pi*rho*b^2*C_k*(a-0.5),...
        rho*b^2*v*T{4}-rho*v*b^2*C_k*T{11},...
        -2*pi*rho*v*b*C_k];
    
    Matrices.F = [2*rho*v^2*b^2*pi*(a+1/2)*C_k,...
        2*rho*v^2*b^2*T{10}*(a+1/2)*C_k-rho*b^2*v^2*(T{4}+T{10}),0;
        -rho*v^2*b^2*T{12}*C_k,...
        -rho*v^2*b^2*(T{5}-T{4}*T{10})/pi-rho*v^2*b^2*T{12}*T{10}*C_k/pi,0;
        -2*pi*rho*v^2*b*C_k, -2*rho*v^2*b*C_k*T{10},0];
end