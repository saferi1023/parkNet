package com.hci;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

/**
 * Servlet implementation class generateBasicItinerary
 */
@WebServlet("/generateBasicItinerary.do")
public class generateBasicItinerary extends HttpServlet {

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		 StringBuilder sb = new StringBuilder();
	        BufferedReader reader = request.getReader();
	        try {
	            String line;
	            while ((line = reader.readLine()) != null) {
	                sb.append(line).append('\n');
	            }
	        } finally {
	            reader.close();
	        }
	        System.out.println(sb);
	        saveJsonToFile(sb.toString(),request);
	        boolean executed = executePython();
	        if(executed) {
	        	String filePath = "itinerary.txt";

	        	try {
	                String content = Files.readString(Paths.get(filePath));
	                ItineraryResponse itineraryResponse = new ItineraryResponse(content);
	                Gson gson = new Gson();
	                String jsonResponse = gson.toJson(itineraryResponse);
	                response.setContentType("application/json");
	                response.getWriter().write(jsonResponse);
	            } catch (IOException e) {
	                e.printStackTrace();
	            }
	        }
	}
	
	class ItineraryResponse {
	    private String itinerary;

	    public ItineraryResponse(String itinerary) {
	        this.itinerary = itinerary;
	    }

	    public String getItinerary() {
	        return itinerary;
	    }

	    public void setItinerary(String itinerary) {
	        this.itinerary = itinerary;
	    }
	}
	
	private boolean executePython() {
		try {
            String pythonCommand = "/opt/anaconda3/bin/python";
            String scriptPath = "/Users/ramunagalla/Desktop/MSCS/Assignments/hci/parknet/ParkNet/src/main/java/com/hci/simple_itinerary.py";
            ProcessBuilder pb = new ProcessBuilder(pythonCommand, scriptPath);
            Process process = pb.start();
            int exitCode = process.waitFor();
            if (exitCode == 0) {
               return true;
            } else {
                System.out.println("Python script execution failed with exit code: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
		return false;
    }
	
	
	 private void saveJsonToFile(String jsonData,HttpServletRequest request) throws IOException {  

     File file = new File("/Users/ramunagalla/desktop/mscs/file.json");

     // Write JSON data to the file
     try (FileWriter writer = new FileWriter(file)) {
         writer.write(jsonData);
     }

     System.out.println("JSON data saved to file: " + file.getAbsolutePath());}

}
