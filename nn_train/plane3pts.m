function [ n_hat, po ] = plane3pts(po1, po2, po3)
    % Define 2 vectors as difference of points
    u = po1 - po3;
    v = po1 - po2;
    % Normalize cross product to obtain normal vector
    no = cross(u, v);
    n_hat = no / norm(no);
    % Force z component to be positive
    % Calculate centroid of 3 points from which to calculate len distances
    po = (po1 + po2 + po3) / 3;
end