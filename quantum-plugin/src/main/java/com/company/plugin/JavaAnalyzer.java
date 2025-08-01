package com.company.plugin;
import java.io.*;
public class JavaAnalyzer {
    public static void main(String[] args) throws Exception {
        File input = new File("../reports/diff.txt");
        File output = new File("../reports/optimized-tests.txt");
        try (BufferedReader br = new BufferedReader(new FileReader(input));
             FileWriter fw = new FileWriter(output)) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.contains("UserService")) fw.write("UserServiceTest\n");
                else if (line.contains("ClaimsService")) fw.write("ClaimsServiceTest\n");
            }
        }
        Runtime.getRuntime().exec("python3 QAOAOptimizer.py").waitFor();
    }
}
