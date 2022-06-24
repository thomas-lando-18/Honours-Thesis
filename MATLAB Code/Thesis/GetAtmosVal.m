function [rho, v] = GetAtmosVal(Alt, Mach)
    % This function will take a selected altitude and Mach number and
    % produce an air density and velocity.
    
    [~, a, ~, rho] = atmosisa(Alt);
    
    v = Mach*a;

end