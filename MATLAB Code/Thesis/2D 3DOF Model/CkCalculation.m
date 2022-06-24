function C = CkCalculation(k)
    % This function is used to caluclate the Bessel function values for the
    % C(k) value in the equation Output: C = [F, G] where C(k) = F+Gi
    if k == 0
        F = 1;
        G = 0;
    elseif 1/k == 0
        F = 0.5;
        G = 0;
    else
    J0 = besselj(0, k);
    J1 = besselj(1, k);
    
    Y0 = bessely(0, k);
    Y1 = bessely(1, k);
    
    F = (J1*(J1+Y0)+Y1*(Y1-J0))/((J1+Y0)^2+(Y1-J0)^2);
    G = -(Y1*Y0+J1*J0)/((J1+Y0)^2+(Y1-J0)^2);
    
    end
    
    C = complex(F, G);
end