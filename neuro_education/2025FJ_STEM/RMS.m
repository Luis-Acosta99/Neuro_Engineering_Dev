max=size(ALLEEG,2);
rawandprepro = true; %set false if ALLEEG does not contain them in sequence

chans = size (ALLEEG(1).data,1)

if rawandprepro == true
    loopsize=max/2;
else
    loopsize=max;
end

for s = 1:loopsize
    % Identify the pair indices: (2*s - 1) is odd, (2*s) is even
    data2 = ALLEEG(s*2).data;     % e.g., Preprocessed (or second signal)

    % Vectorized RMSE calculation for ALL 8 channels simultaneously
    ms = mean(data2.^2, 2);     % Square differences and compute Mean along time (dimension 2)
    rms_vals = sqrt(ms);      % Compute Root
    
    % Store result (transpose to fit 8 channel values into the row)
    rms(s, :) = rms_vals';
end

%%
% 1. Define your channel labels
chan_labels = {'Fz', 'C3', 'Cz', 'C4', 'Pz', 'PO7', 'Oz', 'PO8'};

% 2. Create the Figure
figure('Color', 'w'); % 'w' makes the background white

% 3. Draw the Boxplot
% 'Symbol', '' hides the default outlier markers so we don't plot them twice
boxplot(rms, 'Labels', chan_labels, 'Symbol', ''); 
hold on; 

% 4. Overlay the Data Points (Scatter with Jitter)
% We loop through each channel (column) to plot the points
for c = 1:size(rms, 2)
    % Create x-coordinates centered on the channel number (1, 2, 3...)
    % We add random noise (jitter) between -0.1 and +0.1 to spread them out
    x_center = c;
    jitter_width = 0.2; 
    x_jitter = (rand(size(rms, 1), 1) - 0.5) * jitter_width;
    
    x_values = x_center + x_jitter;
    y_values = rms(:, c);
    
    % Plot the points
    % 'k' = black color, 'filled' makes them solid circles
    scatter(x_values, y_values, 20, 'k', 'filled', 'MarkerFaceAlpha', 0.5);
end

% 5. Styling
ylabel('RMS (\muV)', 'FontSize', 14);
title('Preprocessed RMS voltage', 'FontSize', 16); % Title slightly largergrid on;       % Adds a grid for easier reading
box off;       % Removes the top and right border lines for a cleaner look
hold off;

%%

% 6. Save the Figure as High-Resolution TIFF 🚀
% -dtiff: Device driver for TIFF format
% -r600: Sets the resolution to 600 DPI (high resolution)
print('RMS_OL_Boxplot.tif', '-dtiff', '-r600')