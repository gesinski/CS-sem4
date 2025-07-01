function [rand_counts, counts_mean, circles, a, b, r_max] = generate_circles(n_max)
    a = 250;
    b = 100; 
    r_max = 50;
    
    circles = zeros(n_max, 3);
    rand_counts = zeros(1, n_max);
    counts_mean = zeros(1, n_max);
    counts_sum = 0;

    for i = 1:n_max
        valid = false;
        attempts = 0;
        
        while ~valid
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
            rand_counts(i) = attempts;
            counts_sum = counts_sum + attempts;
            counts_mean(i) = counts_sum / i;
        end
    end

    subplot(2,1,1);
    plot(rand_counts);
    title("Liczba losowań potrzebnych do wyznaczenia parametrów każdego okręgu");
    xlabel("Liczba okręgów");
    ylabel("Losowania");
    subplot(2,1,2);
    plot(counts_mean);
    title("Średnia liczba losowań na kolejnych etapach generowania okręgów");
    xlabel("Liczba okręgów");
    ylabel("Średnia liczba losowań");
end