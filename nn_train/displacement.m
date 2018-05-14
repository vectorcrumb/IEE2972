function [ dp, theta ] = displacement(po1,po2,po3,p1,p2,p3,fd)
%     h_0 = .5*(h_max+h_min);
%     p1(3) = p1(3) + h_0;
%     p2(3) = p2(3) + h_0;
%     p3(3) = p3(3) + h_0;
    % Calculate normal vector and centroid
    [no, po] = plane3pts(po1, po2, po3);
    [n, p] = plane3pts(p1, p2, p3);
    % Obtain angle difference between both vectors
    theta = acosd(dot(no, n));
    % Define the focal distance and find both focal points
    pfo = fd * no + po;
    pf = fd * n + p;
    % Calculate displacements between points
    dp = pf - pfo;
end

