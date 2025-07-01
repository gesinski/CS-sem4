function plot_circles(a, b, circles)
    for i = 1:size(circles, 1)
        plot_circle(circles(i, 3), circles(i, 1), circles(i, 2));
        
        axis equal;
        axis([0 a 0 b]);
        hold on;
    end
end
