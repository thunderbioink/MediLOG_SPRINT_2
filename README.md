# MediLOG_SPRINT_2

# Overview

Working on this new version of MediLOG has allowed me to enjoy using new cloud storage providers such as Firebase by Google and the process needed to create all sorts of Medical Databases.

MediLOG began as an interactive Medical Database, integrated with SQL and Python and is now transitioned to Cloud database storage with Firebase by Google with Python Language. MediLOG is intended for two users: Health Professionals that retrieve patient medication data, and Home Patients that update their Health Provider with their medication dosage and intake times.

Once running the program, the user is displayed with a *Menu*. In this *menu view*, the user can select up to five choices:

### *FULL MAIN MENU DISPLAY:*
![Main Menu](/images/main_menu.png)

1. **Exit Program:**

    * Enter number *"0"* to pick.
    * Exit Program.
2. **Add a New Patient:**

    * Enter number *"1"* to pick.
    * Prompts user to enter the following information:
        * Name
        * Date of birth
        * Diagnosis
        * Illness/Disability
        * Folder creation time and date

3. **Log Medication Intake:**

    * Enter number *"2"* to pick.
    * Prompts user to enter First and Last Name, Medication Name, Dosage, and date and time taken.

4. **Search Patient Database**
    * Enter number *"3"* view different data inputed.
    * This will display an inner MENU where the user can display the following information:
### *Option 3 Menu:*
![Col1](/images/sp_menu3.png)

The purpose of this program is to aid Health proffesionals in the administration of their patient records. This program is the first step into integrating a future patient database, where the patient will be able to log medication, dosage, and intake date and time. These future improvements will automatically update into their existing patient folder.

The idea was originally inspired by individuals that need to constantly update their medically complex family member's medication,dosage, and intake date and time from home. They do this by calling their assigned health professional in plain 2022. One of them was able to express to me how during the pandemic, being able to keep their health provider's updated with their family member's medication intake patterns would be much easier if they had an app to send that information to their existing patient records.

MediLOG's current functionality is the first step into aiding, both, individuals with medically complex family members and professional health providers, enhance their patient record updating experience.


[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

The cloud database used for this program is Firebase by Google. Where you can create a Collection that can contain unique Documents; each with unique Values.  
### *Collection 1, view:*
![Col1](/images/col1.png)

### *Collection 2, view:*
![Col2](/images/col2.png)


With the prior description, the visual organzation scheme for this program's data is in the Document form, where each Collection has it's own set of branches of information:

![Database Input Format](/images/cloudatabase_organize.png)
*Image taken from ["What is a Cloud Database"](https://www.mongodb.com/cloud-database)*

# Development Environment

The development tools used for this program are Firebase by Google, Visual Studio Code, and GitHub.

The programming language used for this program was the integration of Python and Firebase commands.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Firebase](https://firebase.google.com/)
* [No SQL Tutorial](https://www.guru99.com/nosql-tutorial.html)
* [Data Options In the Cloud](https://www.oreilly.com/library/view/an-introduction-to/9781492044857/ch01.html)
* [What is a Cloud Database?](https://www.mongodb.com/cloud-database)
* [Firebase Console](https://firebase.google.com/docs/firestore)
* [Health Database Organization](https://www.ncbi.nlm.nih.gov/books/NBK236556/)
* [Data Elements as a Critical Dimension of Health Care Databases](https://www.ncbi.nlm.nih.gov/books/NBK236556/table/ttt00001/?report=objectonly)
* [Legal Medical Record Standards](https://policy.ucop.edu/doc/1100168/LegalMedicalRecord)
* [Journal of Biomedical Informatics](https://www.sciencedirect.com/science/article/pii/S1532046420302987)
* [The Computer Based Patient Record](https://www.ncbi.nlm.nih.gov/books/NBK233055/)

# Future Work

Improvement for this program:
* Activate Notifications for database changes.
* Activate delete and update logged medication information. 

*Because the app I intend to create based on this program will handle health-related information that will aid health providers monitor their patients medication intake, I need to find I way to safely allow the user to modify their medication logs without deleting the patient itself.*
* Make this program a workable web and phone app for the intended users. This will be a long-term goal. But implementation will begin soon.
