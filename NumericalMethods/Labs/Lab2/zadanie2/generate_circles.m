function [circle_areas, circles, a, b, r_max] = generate_circles(n_max)
    a = 250;
    b = 100;
    r_max = 50;
    
    circles = zeros(n_max, 3);
    circle_areas = zeros(n_max, 1);
    
    S = 0;
    P = a * b;
    
    for i = 1:n_max
        valid = false;
        max_attempts = 1000;
        attempts = 0;
        
        while ~valid && attempts < max_attempts
            attempts = attempts + 1;
            R = rand() * r_max;
            X = rand() * a;
            Y = rand() * b;
            if X - R < 0 || X + R > a || Y - R < 0 || Y + R > b
                continue;
            end
            
            collision = false;
            for j = 1:size(circles, 1)
                X2 = circles(j, 1);
                Y2 = circles(j, 2);
                R2 = circles(j, 3);
                
                distance = sqrt((X - X2)^2 + (Y - Y2)^2);
                if distance < (R + R2)
                    collision = true;
                    break;
                end
                if distance + min(R, R2) <= max(R, R2)
                    collision = true;
                    break;
                end
            end
            
            if ~collision
                valid = true;
            end
        end
      
        if valid
            circles(i, :) = [X, Y, R];

            S = S + pi*R^2;
            circle_areas(i) = (S / P) * 100;
        else
            circles = circles(1:i-1);
            circle_areas = circle_areas(1:i-1);
        end
    end
   
    plot(circle_areas);
    title("Skumulowany stosunek powierzchni kół do powierzchni prostokąta")
    xlabel("Liczba wygenerowanych kół");
    ylabel("Stosunek powierzchni kół do powierzchni prostokąta [%]");
    grid on;
end
