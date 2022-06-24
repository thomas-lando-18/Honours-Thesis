% Thesis Testing and Development

% Mesh Design 

% 2D 
% 2D model recreate

% Airfoil parameters

% Define Foil
BuildTrapWing();

% Build Model

%% Functions

function grid = Trapezoidal_Fin(chord, height, tip_length, tail_length, ...
    no_panels)

    % TODO: add angle of attack
    % TODO: add flap
    
    % Define outline points
    point.tip = [0,0];
    point.tail = [chord, 0];
    point.box = [tip_length, height/2;
                 chord - tail_length, height/2;
                 chord - tail_length, - height/2;
                 tip_length, - height/2];
   
    tip_top = polyfit([point.tip(1, 1), point.box(1, 1)], ...
        [point.tip(1, 2), point.box(1, 2)], 1);
    grid.tip.top(1, :) = linspace(point.tip(1, 1), point.box(1, 1), no_panels);
    grid.tip.top(2, :) = polyval(tip_top, grid.tip.top(1, :));
    
    body_top = polyfit([point.box(1, 1), point.box(2, 1)], ...
        [point.box(1, 2), point.box(2, 2)], 1);
    grid.body.top(1, :) = linspace(point.box(1, 1), point.box(2, 1), no_panels);
    grid.body.top(2, :) = polyval(body_top, grid.body.top(1, :));
    
    tail_top = polyfit([point.box(2, 1), point.tail(1, 1)], ...
        [point.box(2, 2), point.tail(1, 2)], 1);
    grid.tail.top(1, :) = linspace(point.box(2, 1), point.tail(1, 1), no_panels);
    grid.tail.top(2, :) = polyval(tail_top, grid.tail.top(1, :));
    
    % Bottom Surface
    tip_bottom = polyfit([point.tip(1, 1), point.box(4, 1)], ...
        [point.tip(1, 2), point.box(4, 2)], 1);
    grid.tip.bottom(1, :) = linspace(point.tip(1, 1), point.box(4, 1), no_panels);
    grid.tip.bottom(2, :) = polyval(tip_bottom, grid.tip.bottom(1, :));
    
    body_bottom = polyfit([point.box(4, 1), point.box(3, 1)], ...
        [point.box(4, 2), point.box(3, 2)], 1);
    grid.body.bottom(1, :) = linspace(point.box(4, 1), point.box(3, 1), no_panels);
    grid.body.bottom(2, :) = polyval(body_bottom, grid.body.bottom(1, :));
    
    tail_bottom = polyfit([point.box(3, 1), point.tail(1, 1)], ...
        [point.box(3, 2), point.tail(1, 2)], 1);
    grid.tail.bottom(1, :) = linspace(point.box(3, 1), point.tail(1, 1), no_panels);
    grid.tail.bottom(2, :) = polyval(tail_bottom, grid.tail.bottom(1, :));
    
end

function Plot_Surface(top, bottom)

    figure()
    grid on
    hold on
    plot(top(1,:), top(2,:), 'b');
    plot(bottom(1,:), bottom(2,:), 'b');
    axis equal
    
end

function BuildTrapWing()
    % Trapezoidal
    chord = input('input chord length (m): ');
    tip_length = input('input tip length (m): ');
    tail_length = input('input tail length (m): ');
    height = input('input fin thickness (m): ');
    no_panels = input('input no. panels per side: ');
    fprintf...
        ('Further Developments will provide a specified total no. panels\n');

    mesh_points = Trapezoidal_Fin(chord, height, tip_length, tail_length,...
        no_panels);

    top_surface = [mesh_points.tip.top(1,:), mesh_points.body.top(1,:),...
        mesh_points.tail.top(1,:);
        mesh_points.tip.top(2,:), mesh_points.body.top(2,:), ...
        mesh_points.tail.top(2,:)];
    bottom_surface = [mesh_points.tip.bottom(1,:), mesh_points.body.bottom(1,:),...
        mesh_points.tail.bottom(1,:);
        mesh_points.tip.bottom(2,:), mesh_points.body.bottom(2,:), ...
        mesh_points.tail.bottom(2,:)];

    Plot_Surface(top_surface, bottom_surface);
end