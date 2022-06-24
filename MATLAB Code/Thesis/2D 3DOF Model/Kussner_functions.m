function P = Kussner_functions(phi)
    P{1} = pi- phi+sin(phi);
    P{2} = (pi-phi)*(1+2*cos(phi))+sin(phi)*(2+cos(phi));
    P{3} = pi - phi + sin(phi)*cos(phi);
    P{4} = (pi- phi)*2*cos(phi) + sin(phi)*2/3*(2+(cos(phi))^2);
    P{5} = sin(phi)*(1-cos(phi));
    P{6} = 2*(pi-phi)+sin(phi)*2/3*(2-cos(phi))*(1+2*cos(phi));
    P{7} = (pi-phi)*(1/2+2*cos(phi))+sin(phi)*1/6*(8+5*cos(phi)-4*...
        (cos(phi))^2-2*(cos(phi))^3);
    P{8} = 
end