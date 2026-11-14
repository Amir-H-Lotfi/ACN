clc;
clear;
close all;

% Resolve directories
ROOT = fileparts(fileparts(fileparts(mfilename("fullpath"))));

DATA = fullfile(ROOT, "data", "processed");
PLOT = fullfile(ROOT, "matlab", "plots");
REPORT = fullfile(ROOT, "reports", "ml.plots");

MATLAB = fileparts(fileparts(mfilename("fullpath")));
FUNCTION=fullfile(MATLAB,"src","functions");

% Inject source codes
addpath(FUNCTION);

data_files = dir(fullfile(DATA,"*.csv"));

DISTANCE_CM = 10;
DISTANCE_M = 0.1;

datasets = containers.Map(...
    "KeyType","char", ...
    "ValueType" , "any" ...
    );

axis_pairs = {
    'wn' , 'kna';
    'fthz', 'kna';
    'fthz' , 'al';
    'fthz' , 'sl';
    'fthz', 'tl'
    };

axis_labels = struct ( ...
    'wn' ,"Wavenumber (cm^{-1})", ...
    'kna', "Absorption Coefficient (cm^{-1})", ...
    'fthz', 'Frequency (THz)',...
    'al' ,'Inversion Transmittance (dimensionless)', ...
    'sl', 'Spreading Loss (dB)', ...
    'tl', 'Total path loss (dB)' ...
    );

for i = 1:numel(data_files)
    current_filename = fullfile(DATA , data_files(i).name);
    
    raw_data =readmatrix(current_filename, "NumHeaderLines" , 1);
    
    % Extract oriinal vectors
    wn = raw_data(:,1);
    kna = raw_data(:,2);
    ka = raw_data(:,3);
    
    % Calculate derived vectors
    fhz = wnTohz(wn);
    fthz = wnTothz(wn);
    
    al = absorption_loss(kna,DISTANCE_CM);
    sl = spreading_loss(fhz , DISTANCE_M);
    
    % just a change in scale and dimension, nothing personal !
    al_db = 10 .* log10(al);
    tl = total_loss(al_db ,sl);
    
    % Extract original filename
    [~,srcname,~] = fileparts(data_files(i).name);
    
    % Bundle all vectors
    records = struct(...
        'sourcefile',data_files(i).name, ...
        'sourceName', srcname, ...
        'wn', wn, ...
        'kna',kna, ...
        'ka', ka, ...
        'fhz' , fhz, ...
        'fthz', fthz,...
        'al', al , ...
        'al_db' , al_db , ...
        'sl', sl, ...
        'tl', tl ...
        );
    
    % Store a dataset with a short key
    datasets(srcname) = records;
    
    % Create output directory
    output_plot_dir = fullfile(PLOT,records.sourceName + "_plot");
    
    if ~isfolder(output_plot_dir)
        mkdir(output_plot_dir);
    end
    
    report_plot_dir = fullfile(REPORT ,records.sourceName + "_plot");
    
    if ~isfolder(report_plot_dir)
        mkdir(report_plot_dir);
    end
    
    % Create requested plots
    
    for p= 1:size(axis_pairs,1)
        xAxis_name = axis_pairs{p,1};
        yAxis_name = axis_pairs{p,2};
        
        x= records.(xAxis_name);
        y= records.(yAxis_name);
        
        % Create figure
        fig = figure("Visible" , "off");
        
        plot(x,y, "LineWidth",1.5);
        
        % xticks(linspace(min(x) , max(x), 20))
        
        xlabel(axis_labels.(xAxis_name));
        ylabel(axis_labels.(yAxis_name));
        
        % title(sprintf("%s: %s vs %s" ,...
        %     srcname , yname , xname), ...
        %     "Interpreter","none")
        plot_title = title(sprintf("%s vs %s", ...
            char(axis_labels.(yAxis_name)) , ...
            char(axis_labels.(xAxis_name)) ...
            ), ...
            "Interpreter", ...
            "tex" ...
            );
        plot_title.FontSize = 8;
        plot_title.FontWeight ='normal';
        
        
        grid on;
        
        % generate output filename
        string_output_filename = sprintf("%s_plot.%s.%s.png", ...
            srcname , xAxis_name, yAxis_name);
        
        % export plot
        output_file = fullfile(output_plot_dir, string_output_filename);
        exportgraphics(fig,output_file, "Resolution" , 300);
        
        % a copy into report directory is neeeded
        report_file = fullfile(report_plot_dir,string_output_filename);
        copyfile(output_file, report_file);
        
        % Release figure resources
        close(fig);
    end
    
end



