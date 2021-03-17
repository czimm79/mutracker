input_folder = "C:/Wormhole/OneDrive/Python/public mutracker/mutracker/original_video"
output_folder = "C:/Wormhole/OneDrive/Python/public mutracker/mutracker/imagej_data"
outline_folder = "C:/Wormhole/OneDrive/Python/public mutracker/mutracker/imagej_outline_videos"

// min_size calculation and explanation
// For wheel videos at 10x, 1.25t, mpp = 0.667
// I want to exclude imaging artifacts (dust, speck on cambera) that would be less than a monomer, accounting for
// optical imaging artifacts. The corona of the colloid extends to about 1.5sigma, or 6.75 um diameter.
// For wheel videos, the area of a 6.75 um particle would be 80.435 pix^2. Round down to 80.
// For logan 4x 2t, mpp= 1.618.
min_size = 80

THRESHOLD = 7913  // ONLY used if constant threshold binary is enabled. Commented out by default.

function batch(input_folder, output_folder, outline_folder) {
	// Looks inside input_folder and for each image stack, uses the process function on it.
	list = getFileList(input_folder);
	for (i = 0; i < list.length; i++){
		name = substring(list[i], 0, lengthOf(list[i]) - 1);  // removes trailing bracket
        process(name, input_folder, output_folder, outline_folder);
}
}

function process(stack_name, input_folder, output_folder, outline_folder) {
	// Do image processing on stack_name and output results in a csv to output_folder.
	stack_path = input_folder + "/" + stack_name;
	output_path = output_folder + "/" + stack_name + ".csv";
	outline_path = outline_folder + "/" + stack_name + "/a.tif";
	outline_directory = outline_folder + "/" + stack_name;
	
	// Process
	run("Image Sequence...", "open=stack_path sort");

	// Constant threshold binary
//	run("Threshold...");
//	setThreshold(0, THRESHOLD);
//	setOption("BlackBackground", true);
//	run("Convert to Mask", "method=Default background=Light calculate black");
//	run("Close");

	// Other way of making binary without choosing a threshold. Works similar, can use this if wanted.
	run("Make Binary", "method=Default background=Default calculate black");
	
	run("Set Measurements...", "area centroid center fit display redirect=None decimal=3");
	run("Analyze Particles...", "size=min_size-Infinity show=Outlines display clear stack");


	// Save outlines
	File.makeDirectory(outline_directory);
	run("Image Sequence... ", "format=TIFF name=a save=outline_path");
	close();

	
	saveAs("Results", output_path);
	close();
	
}


batch(input_folder, output_folder, outline_folder)