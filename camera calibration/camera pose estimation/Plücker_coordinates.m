% MATLAB Script: Visualizing Plücker Coordinates Geometric Interpretation
clear; clc; close all;

%% 1. Define Points and Compute Plücker Coordinates
% Two points defining the line (from our numerical example)
A_cart = [1; 2; 0];
B_cart = [0; 3; 2];

% Appending 1 for homogeneous form
A = [A_cart; 1];
B = [B_cart; 1];

% Compute Plücker elements (p_ij = A_i*B_j - A_j*B_i)
p12 = A(1)*B(2) - A(2)*B(1);
p13 = A(1)*B(3) - A(3)*B(1);
p14 = A(1)*B(4) - A(4)*B(1);
p23 = A(2)*B(3) - A(3)*B(2);
p42 = A(4)*B(2) - A(2)*B(4);
p34 = A(3)*B(4) - A(4)*B(3);

% Extract standard 3D vectors
% Direction vector d = B_cart - A_cart = [p14; p24; p34]
d = [p14; -p42; p34]; 
% Moment vector m = A_cart x B_cart = [p23; p31; p12]
m = [p23; -p13; p12]; 

%% 2. Set Up Figure and Plots
figure('Color', 'w', 'Position', [100, 100, 850, 650]);
hold on; grid on; axis equal;
view(3); % Change to standard 3D viewing angle

% Plot the coordinate origin
plot3(0, 0, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8, 'DisplayName', 'Origin (O)');

% Plot Point A and Point B
plot3(A_cart(1), A_cart(2), A_cart(3), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 8, 'DisplayName', 'Point A (1,2,0)');
plot3(B_cart(1), B_cart(2), B_cart(3), 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 8, 'DisplayName', 'Point B (0,3,2)');

%% 3. Plot the Infinite Line 
% Extrapolate beyond segments A and B to show the actual structural line
t = linspace(-1.5, 2.5, 100);
line_x = A_cart(1) + t * d(1);
line_y = A_cart(2) + t * d(2);
line_z = A_cart(3) + t * d(3);
plot3(line_x, line_y, line_z, 'k--', 'LineWidth', 1.5, 'DisplayName', 'Line L');

%% 4. Plot Vectors (Using quiver3)
% Position vectors from Origin to A and B (Thin gray lines)
quiver3(0, 0, 0, A_cart(1), A_cart(2), A_cart(3), 0, 'Color', [0.5 0.5 0.5], 'LineStyle', ':', 'LineWidth', 1.2, 'DisplayName', 'Position vector a');
quiver3(0, 0, 0, B_cart(1), B_cart(2), B_cart(3), 0, 'Color', [0.5 0.5 0.5], 'LineStyle', ':', 'LineWidth', 1.2, 'DisplayName', 'Position vector b');

% Direction Vector d (Plotted directly resting on top of the line segment AB)
quiver3(A_cart(1), A_cart(2), A_cart(3), d(1), d(2), d(3), 0, 'r', 'LineWidth', 2.5, 'MaxHeadSize', 0.5, 'DisplayName', 'Direction Vector d (b-a)');

% Moment Vector m (Plotted originating straight out from the Origin)
quiver3(0, 0, 0, m(1), m(2), m(3), 0, 'm', 'LineWidth', 2.5, 'MaxHeadSize', 0.5, 'DisplayName', 'Moment Vector m (a x b)');

%% 5. Annotations & Scene Enhancements
% Add text labels next to features
text(0.1, 0.1, 0.1, ' O', 'FontSize', 12, 'FontWeight', 'bold');
text(A_cart(1)+0.1, A_cart(2), A_cart(3), ' A', 'FontSize', 12, 'Color', 'r');
text(B_cart(1)+0.1, B_cart(2), B_cart(3), ' B', 'FontSize', 12, 'Color', 'b');
text(A_cart(1) + 0.5*d(1), A_cart(2) + 0.5*d(2) + 0.2, A_cart(3) + 0.5*d(3), ' \bf{d}', 'FontSize', 14, 'Color', 'r');
text(0.5*m(1), 0.5*m(2), 0.5*m(3) + 0.3, ' \bf{m}', 'FontSize', 14, 'Color', 'm');

% Label axes
xlabel('X Axis', 'FontSize', 11);
ylabel('Y Axis', 'FontSize', 11);
zlabel('Z Axis', 'FontSize', 11);
title('Geometric Interpretation of Plücker Coordinates: p = (m, d)', 'FontSize', 14);

% Final configuration
legend('Location', 'bestoutside');
xlim([-1, 5]); ylim([-1, 5]); zlim([-1, 5]);
hold off;
