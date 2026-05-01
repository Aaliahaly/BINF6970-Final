CREATE TABLE Patient (
    Patient_ID VARCHAR(30) PRIMARY KEY,
    Gender VARCHAR(10),
    Genetic_Ancestry_Label VARCHAR(15)
);

CREATE TABLE Cancer (
    Cancer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Cancer_Site VARCHAR(50),
    Cancer_Type VARCHAR(50),
    Cancer_Histological_Type VARCHAR(50)
);

CREATE TABLE Diagnosis (
    Diagnosis_ID INT PRIMARY KEY AUTO_INCREMENT,
    Patient_ID VARCHAR(30),
    Cancer_ID INT,
    Diagnosis_Age TINYINT UNSIGNED,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Cancer_ID) REFERENCES Cancer(Cancer_ID)
);

CREATE TABLE Survival (
    Survival_ID INT PRIMARY KEY AUTO_INCREMENT,
    Diagnosis_ID INT,
    Overall_Survival_Status VARCHAR(30),
    Overall_Survival_Months DECIMAL(6,2),
    Disease_Free_Status VARCHAR(30),
    Disease_Free_Months DECIMAL(6,2),
    Progression_Free_Status VARCHAR(30),
    Progression_Free_Months DECIMAL(6,2),
    Disease_Specific_Survival_Status VARCHAR(30),
    Disease_Specific_Survival_Months DECIMAL(6,2),
    FOREIGN KEY (Diagnosis_ID) REFERENCES Diagnosis(Diagnosis_ID)
);

CREATE TABLE Sample (
    Sample_ID VARCHAR(30) PRIMARY KEY,
    Diagnosis_ID INT,
    Sample_Type VARCHAR(20),
    Tumor_Histologic_Grade VARCHAR(5),
    Aneuploidy_Score TINYINT UNSIGNED,
    Somatic_Status VARCHAR(20),
    IDH_Status VARCHAR(20),
    Codeletion_Status VARCHAR(20),
    FOREIGN KEY (Diagnosis_ID) REFERENCES Diagnosis(Diagnosis_ID)
);

CREATE TABLE Gene (
    Gene_ID INT PRIMARY KEY AUTO_INCREMENT,
    Entrez_Gene_ID INT,
    Hugo_Symbol VARCHAR(50)
);

CREATE TABLE Mutation (
    Mutation_ID INT PRIMARY KEY AUTO_INCREMENT,
    Gene_ID INT,
    Chromosome VARCHAR(5),
    Start_Position INT,
    End_Position INT,
    Reference_Allele VARCHAR(150),
    Tumor_Seq_Allele VARCHAR(150),
    Variant_Type VARCHAR(50),
    Variant_Classification VARCHAR(50),
    Primary_Consequence VARCHAR(50),
    Impact_Level VARCHAR(30),
    FOREIGN KEY (Gene_ID) REFERENCES Gene(Gene_ID)
);

CREATE TABLE Sample_Mutation (
    Mutation_ID INT,
    Sample_ID VARCHAR(30),
    VAF DECIMAL(6,2),
    PRIMARY KEY (Mutation_ID, Sample_ID),
    FOREIGN KEY (Mutation_ID) REFERENCES Mutation(Mutation_ID),
    FOREIGN KEY (Sample_ID) REFERENCES Sample(Sample_ID)
);

CREATE TABLE Copy_Number_Alteration (
    CNA_ID INT PRIMARY KEY AUTO_INCREMENT,
    Sample_ID VARCHAR(30),
    Gene_ID INT,
    CNA_Value TINYINT,
    CNA_Status VARCHAR(30),
    FOREIGN KEY (Sample_ID) REFERENCES Sample(Sample_ID),
    FOREIGN KEY (Gene_ID) REFERENCES Gene(Gene_ID)
);

CREATE TABLE Expression (
    Sample_ID VARCHAR(30),
    Gene_ID INT,
    Expression_Type VARCHAR(50),
    Expression_Value DECIMAL(10,2),
    PRIMARY KEY (Sample_ID, Gene_ID),
    FOREIGN KEY (Sample_ID) REFERENCES Sample(Sample_ID),
    FOREIGN KEY (Gene_ID) REFERENCES Gene(Gene_ID)
);

CREATE TABLE Sample_Features_Definition (
    Feature_ID INT PRIMARY KEY AUTO_INCREMENT,
    Feature_Name VARCHAR(50)
);

CREATE TABLE Sample_Feature (
    Feature_ID INT,
    Sample_ID VARCHAR(30),
    Value INT,
    PRIMARY KEY (Feature_ID, Sample_ID),
    FOREIGN KEY (Feature_ID) REFERENCES Sample_Features_Definition(Feature_ID),
    FOREIGN KEY (Sample_ID) REFERENCES Sample(Sample_ID)
);
