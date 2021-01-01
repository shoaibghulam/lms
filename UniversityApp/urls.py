from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    # faculty
    path('', views.index,name="uniadmin"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('branch', views.branch,name="branch"),
    path('profile', views.profile,name="profile"),
    path('faculty', views.faculty,name="faculty"),
    path('student', views.student,name="student"),
    path('contact', views.contact,name="contact"),
    path('assignment', views.assignment,name="assignment"),
    path('addassignment', views.addassignment,name="addassignment"), 
    path('admincoursevideo', views.admincoursevideo,name="admincoursevideo"),
    path('admincoursef', views.admincoursef,name="admincoursef"),
    path('admindepartment', views.admindepartment,name="admindepartment"),
    path('adminexamresult', views.adminexamresult,name="adminexamresult"),
    path('adminfacultydevelopment', views.adminfacultydevelopment,name="adminfacultydevelopment"),
    path('adminfacultyeval', views.adminfacultyeval,name="adminfacultyeval"),
    path('admininstructor', views.admininstructor,name="admininstructor"),
    path('adminmaterialclass', views.adminmaterialclass,name="adminmaterialclass"),
    path('adminnotificationmodel', views.adminnotificationmodel,name="adminnotificationmodel"),
    path('adminonlinequiz', views.adminonlinequiz,name="adminonlinequiz"),
    path('adminqueryadmin', views.adminqueryadmin,name="adminqueryadmin"),
    path('adminsemes', views.adminsemes,name="adminsemes"),
    path('adminteacherapplication', views.adminteacherapplication,name="adminteacherapplication"),
    path('adminteachersyllabus', views.adminteachersyllabus,name="adminteachersyllabus"),
    path('adminusersignup', views.adminusersignup,name="adminusersignup"),
    path('adminuserstory', views.adminuserstory,name="adminuserstory"),
    path('adminadddepartmentf', views.adminadddepartmentf,name="adminadddepartmentf"),
    path('adminaddinstructor', views.adminaddinstructor,name="adminaddinstructor"),
    path('adminaddsemes', views.adminaddsemes,name="adminaddsemes"),
    path('adminaddteacherapp', views.adminaddteacherapp,name="adminaddteacherapp"),
    path('adminaddteachsyllabus', views.adminaddteachsyllabus,name="adminaddteachsyllabus"),
    path('adminaddusersign', views.adminaddusersign,name="adminaddusersign"),
    path('deletesignup/<int:id>', views.deletesignup,name="deletesignup"),
    path('editsignup/<int:id>', views.editsignup,name="editsignup"),
    path('deleteinstructor/<int:id>', views.deleteinstructor,name="deleteinstructor"),
    path('deletedepart/<int:id>', views.deletedepart,name="deletedepart"),
    path('editdepart/<int:id>', views.editdepart,name="editdepart"),
    path('deletesem/<int:id>', views.deletesem,name="deletesem"),
    path('deletecourse/<int:id>', views.deletecourse,name="deletecourse"),
    path('deleteassignmemt/<int:id>', views.deleteassignmemt,name="deleteassignmemt"),
    path('deletecoursevideo/<int:id>', views.deletecoursevideo,name="ddeletecoursevideo"),
    path('deletefacultydevelopment/<int:id>', views.deletefacultydevelopment,name="deletefacultydevelopment"),
    path('deletematerial/<int:id>', views.deletematerial,name="deletematerial"),
    path('adminaddcoursef', views.adminaddcoursef,name="adminaddcoursef"),
    path('admineditexamresult/<int:id>', views.admineditexamresult,name="admineditexamresult"),
    path('deletestudentresult/<int:id>', views.deletestudentresult,name="deletestudentresult"),
    path('adminaddfacultyeval', views.adminaddfacultyeval,name="adminaddfacultyeval"),
    path('deleteFacultyEvalution/<int:id>', views.deleteFacultyEvalution,name="deleteFacultyEvalution"),
    path('admineditfacultyeval/<int:id>', views.admineditfacultyeval,name="admineditfacultyeval"),
    path('deletenotification/<int:id>', views.deletenotification,name="deletenotification"),
    path('deletequiz/<int:id>', views.deletequiz,name="deletequiz"),
    path('admineditqueryadmin/<int:id>', views.admineditqueryadmin,name="admineditqueryadmin"),
    path('deletequery/<int:id>', views.deletequery,name="deletequery"),
    path('deleteapplication/<int:id>', views.deleteapplication,name="deleteapplication"),
    path('editteacherapplication/<int:id>', views.editteacherapplication,name="editteacherapplication"),
    path('deleteteachersyllabus/<int:id>', views.deleteteachersyllabus,name="deleteteachersyllabus"),
    path('Editsyllabus/<int:id>', views.Editsyllabus,name="Editsyllabus"),
    path('Editsyllabus/<int:id>', views.Editsyllabus,name="Editsyllabus"),
    path('deleteFacultyUserStories/<int:id>', views.deleteFacultyUserStories,name="deleteFacultyUserStories"),
    path('Editcourse/<int:id>', views.Editcourse,name="Editcourse"),
    path('contactshow', views.contactshow,name="contactshow"),
    path('deleteContact/<int:id>', views.deleteContact,name="deleteContact"),
    path('signupSuggestion', views.signupSuggestion,name="signupSuggestion"),
    path('ExamEmailSuggestion', views.ExamEmailSuggestion,name="ExamEmailSuggestion"),


    
    





    

    


    


   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    # student
    path('adminapplication', views.adminapplication,name="adminapplication"),
    path('deleteadminapplication/<int:id>', views.deleteadminapplication,name="deleteadminapplication"),
    path('Suggestionadminapplication', views.Suggestionadminapplication,name="Suggestionadminapplication"),

    path('adminjob', views.adminjob,name="adminjob"),
    path('deleteadminjob/<int:id>', views.deleteadminjob,name="deleteadminjob"),
    path('Suggestionadminjob', views.Suggestionadminjob,name="Suggestionadminjob"),

    path('adminmeeting', views.adminmeeting,name="adminmeeting"),
    path('deleteadminmeeting/<int:id>', views.deleteadminmeeting,name="deleteadminmeeting"),
    path('Suggestionadminmeeting', views.Suggestionadminmeeting,name="Suggestionadminmeeting"),

    path('adminregister', views.adminregister,name="adminregister"),
    path('deleteadminregister/<int:id>', views.deleteadminregister,name="deleteadminregister"),
    path('adminaddregister', views.adminaddregister,name="adminaddregister"),
    path('editadminaddregister/<int:id>', views.editadminaddregister,name="editadminaddregister"),
    path('Suggestionadminregister', views.Suggestionadminregister,name="Suggestionadminregister"),

    path('adminscruntiy', views.adminscruntiy,name="adminscruntiy"),
    path('deleteadminscruntiy/<int:id>', views.deleteadminscruntiy,name="deleteadminscruntiy"),
    path('Suggestionadminscruntiy', views.Suggestionadminscruntiy,name="Suggestionadminscruntiy"),

    path('adminassignmet', views.adminassignmet,name="adminassignmet"),
    path('deleteadminassignmet/<int:id>', views.deleteadminassignmet,name="deleteadminassignmet"),
    path('Suggestionadminassignmet', views.Suggestionadminassignmet,name="Suggestionadminassignmet"),

    path('adminquery', views.adminquery,name="adminquery"),
    path('deleteadminquery/<int:id>', views.deleteadminquery,name="deleteadminquery"),
    path('Suggestionadminquery', views.Suggestionadminquery,name="Suggestionadminquery"),

    
    path('adminstudentevalution', views.adminstudentevalution,name="adminstudentevalution"),
    path('deleteadminstudentevalution/<int:id>', views.deleteadminstudentevalution,name="deleteadminstudentevalution"),
    path('Suggestionadminstudentevalution', views.Suggestionadminstudentevalution,name="Suggestionadminstudentevalution"),

    path('adminsurveryans', views.adminsurveryans,name="adminsurveryans"),
    path('deleteadminsurveryans/<int:id>', views.deleteadminsurveryans,name="deleteadminsurveryans"),
    path('Suggestionadminsurveryans', views.Suggestionadminsurveryans,name="Suggestionadminsurveryans"),


    path('admincourse', views.admincourse,name="admincourse"),
    path('AdminAddCourses', views.AdminAddCourses,name="AdminAddCourses"),

    path('adminsprofile', views.adminsprofile,name="adminsprofile"),
    path('Suggadminsprofile', views.Suggadminsprofile,name="Suggadminsprofile"),
    path('deleteadminsprofile/<int:id>', views.deleteadminsprofile,name="deleteadminsprofile"),

    path('adminsignup', views.adminsignup,name="adminsignup"),
    path('Suggestionadminsignup', views.Suggestionadminsignup,name="Suggestionadminsignup"),
    path('deleteadminsignup/<int:id>', views.deleteadminsignup,name="deleteadminsignup"),
    path('adminaddsignup', views.adminaddsignup,name="adminaddsignup"),
    path('editadminsignup/<int:id>', views.editadminsignup,name="editadminsignup"),

    

    
    
    #student shakeeb work

    path('admineditquery', views.admineditquery,name="admineditquery"),
    path('deleteCourse', views.deleteCourse,name="deleteCourse"),
    path('deleteCourseID/<int:id>', views.deleteCourseID,name="deleteCourseID"),



    

    
    
    
    
    
    
    
    
    
    #library
    path('bookauther', views.bookauther,name="bookauther"),
    path('bookauthorSuggestion', views.bookauthorSuggestion,name="bookauthorSuggestion"),
    path('adminaddbookauthor', views.adminaddbookauthor,name="adminaddbookauthor"),
    path('deleteadminaddbookauthor/<int:id>', views.deleteadminaddbookauthor,name="deleteadminaddbookauthor"),
    path('editadminaddbookauthor/<int:id>', views.editadminaddbookauthor,name="editadminaddbookauthor"),
    path('book', views.book,name="book"),
    path('bookSuggestion', views.bookSuggestion,name="bookSuggestion"),
    path('adminaddbook', views.adminaddbook,name="adminaddbook"),
    path('deleteadminaddbook/<int:id>', views.deleteadminaddbook,name="deleteadminaddbook"),
    path('editadminaddbook/<int:id>', views.editadminaddbook,name="editadminaddbook"),


    #admin
    path('academiccalendarmodel', views.academiccalendarmodel,name="academiccalendarmodel"),
    path('academiccalendarmodelSuggestion', views.academiccalendarmodelSuggestion,name="academiccalendarmodelSuggestion"),
    path('newcalendarmodel', views.newcalendarmodel,name="newcalendarmodel"),
    path('editcalendarmodel/<int:id>', views.editcalendarmodel,name="editcalendarmodel"),
    path('deletecalendarmodel/<int:id>', views.deletecalendarmodel,name="deletecalendarmodel"),

    path('adminfacultycalendar', views.adminfacultycalendar,name="adminfacultycalendar"),
    path('adminfacultycalendarSuggestion', views.adminfacultycalendarSuggestion,name="adminfacultycalendarSuggestion"),
    path('adminaddfacultycalendar', views.adminaddfacultycalendar,name="adminaddfacultycalendar"),
    path('admineditfacultycalendar/<int:id>', views.admineditfacultycalendar,name="admineditfacultycalendar"),
    path('deletefacultycalendarmodel/<int:id>', views.deletefacultycalendarmodel,name="deletefacultycalendarmodel"),

    path('adminexam', views.adminexam,name="adminexam"),
    path('adminexamSuggestion', views.adminexamSuggestion,name="adminexamSuggestion"),
    path('addadminexam', views.addadminexam,name="addadminexam"),
    path('admineditexam/<int:id>', views.admineditexam,name="admineditexam"),
    path('deleteadminexam/<int:id>', views.deleteadminexam,name="deleteadminexam"),

    path('adminsemester', views.adminsemester,name="adminsemester"),
    path('adminsemesterSuggestion', views.adminsemesterSuggestion,name="adminsemesterSuggestion"),
    path('adminaddsemesterexm', views.adminaddsemesterexm,name="adminaddsemesterexm"),
    path('admineditsemeterexm/<int:id>', views.admineditsemeterexm,name="admineditsemeterexm"),
    path('deleteadminsemester/<int:id>', views.deleteadminsemester,name="deleteadminsemester"),

    path('adminfacultyattendance', views.adminfacultyattendance,name="adminfacultyattendance"),
    path('adminfacultyattendanceSuggestion', views.adminfacultyattendanceSuggestion,name="adminfacultyattendanceSuggestion"),
    path('adminaddfacultyatten', views.adminaddfacultyatten,name="adminaddfacultyatten"),
    path('admineditfacultyattendance/<int:id>', views.admineditfacultyattendance,name="admineditfacultyattendance"),
    path('deleteadminfacultyattendance/<int:id>', views.deleteadminfacultyattendance,name="deleteadminfacultyattendance"),

    path('adminnotification', views.adminnotification,name="adminnotification"),
    path('adminnotificationSuggestion', views.adminnotificationSuggestion,name="adminnotificationSuggestion"),
    path('adminaddnoti', views.adminaddnoti,name="adminaddnoti"),
    path('Editnotificationmodel/<int:id>', views.Editnotificationmodel,name="Editnotificationmodel"),
    path('deletenotificationmodel/<int:id>', views.deletenotificationmodel,name="deletenotificationmodel"),

    path('adminstudentattendance', views.adminstudentattendance,name="adminstudentattendance"),
    path('adminstudentattendanceSuggestion', views.adminstudentattendanceSuggestion,name="adminstudentattendanceSuggestion"),
    path('adminaddStudentatten', views.adminaddStudentatten,name="adminaddStudentatten"),
    path('admineditStudentattendance/<int:id>', views.admineditStudentattendance,name="admineditStudentattendance"),
    path('deleteadminstudentattendance/<int:id>', views.deleteadminstudentattendance,name="deleteadminstudentattendance"),

    path('adminfacultyevaluation', views.adminfacultyevaluation,name="adminfacultyevaluation"),
    path('addadminfacultyevaluation', views.addadminfacultyevaluation,name="addadminfacultyevaluation"),
    path('adminfacultyevaluationSuggestion', views.adminfacultyevaluationSuggestion,name="adminfacultyevaluationSuggestion"),
    path('deletefacultyevaluation/<int:id>', views.deletefacultyevaluation,name="deletefacultyevaluation"),
    path('editadminfacultyevaluation', views.editadminfacultyevaluation,name="editadminfacultyevaluation"),
    path('show', views.show,name="show"),
    
    path('adminform', views.adminform,name="adminform"),
    path('addadminform', views.addadminform,name="addadminform"),
    path('adminformSuggestion', views.adminformSuggestion,name="adminformSuggestion"),
    path('deleteadminform/<int:id>', views.deleteadminform,name="deleteadminform"),
    path('editadminform', views.editadminform,name="editadminform"),
    path('showform', views.showform,name="showform"),

    path('adminrole', views.adminrole,name="adminrole"),
    path('addadminrole', views.addadminrole,name="addadminrole"),
    path('adminroleSuggestion', views.adminroleSuggestion,name="adminroleSuggestion"),
    path('deleteadminrole/<int:id>', views.deleteadminrole,name="deleteadminrole"),
    path('editrole', views.editrole,name="editrole"),
    path('showrole', views.showrole,name="showrole"),

    path('adminroom', views.adminroom,name="adminroom"),
    path('addadminroom', views.addadminroom,name="addadminroom"),
    path('Suggestionadminroom', views.Suggestionadminroom,name="Suggestionadminroom"),
    path('deleteadminroom/<int:id>', views.deleteadminroom,name="deleteadminroom"),
    path('adminroom', views.adminroom,name="adminroom"),
    path('editroom', views.editroom,name="editroom"),
    path('showroom', views.showroom,name="showroom"),

    path('adminplacementportal', views.adminplacementportal,name="adminplacementportal"),
    path('addadminplacementportal', views.addadminplacementportal,name="addadminplacementportal"),
    path('Suggestionadminplacementportal', views.Suggestionadminplacementportal,name="Suggestionadminplacementportal"),
    path('deleteadminplacementportal/<int:id>', views.deleteadminplacementportal,name="deleteadminplacementportal"),
    path('editadminplacementportal', views.editadminplacementportal,name="editadminplacementportal"),
    path('showplacementportal', views.showplacementportal,name="showplacementportal"),


    path('adminmenuitem', views.adminmenuitem,name="adminmenuitem"),
    path('addadminmenuitem', views.addadminmenuitem,name="addadminmenuitem"),
    path('Suggestionadminmenuitem', views.Suggestionadminmenuitem,name="Suggestionadminmenuitem"),
    path('deleteadminmenuitem/<int:id>', views.deleteadminmenuitem,name="deleteadminmenuitem"),
    path('editadminmenuitem', views.editadminmenuitem,name="editadminmenuitem"),
    path('showmenu', views.showmenu,name="showmenu"),

    path('adminmenuorder', views.adminmenuorder,name="adminmenuorder"),
    path('Suggestionadminmenuorder', views.Suggestionadminmenuorder,name="Suggestionadminmenuorder"),
    path('adminaddorder', views.adminaddorder,name="adminaddorder"),
    path('admineditorder/<int:id>', views.admineditorder,name="admineditorder"),
    path('deletemenuorder/<int:id>', views.deletemenuorder,name="deletemenuorder"),

    path('adminroomreservation', views.adminroomreservation,name="adminroomreservation"),
    path('Suggestionadminroomreservation', views.Suggestionadminroomreservation,name="Suggestionadminroomreservation"),
    path('adminaddroomres', views.adminaddroomres,name="adminaddroomres"),
    path('admineditroomreservation/<int:id>', views.admineditroomreservation,name="admineditroomreservation"),
    path('deleteadminroomreservation/<int:id>', views.deleteadminroomreservation,name="deleteadminroomreservation"),

    path('adminsurvery', views.adminsurvery,name="adminsurvery"),
    path('Suggestionadminsurvery', views.Suggestionadminsurvery,name="Suggestionadminsurvery"),
    path('adminaddsurvey', views.adminaddsurvey,name="adminaddsurvey"),
    path('admineditsurvey/<int:id>', views.admineditsurvey,name="admineditsurvey"),
    path('deleteadminsurvery/<int:id>', views.deleteadminsurvery,name="deleteadminsurvery"),
    
    path('admindashboard', views.admindashboard,name="admindashboard"),


   
    


# add urls by shoaib ghulam
    path('adminbatch',views.adminbatch,name="adminbatch"),
    path('getbatchdata',views.getbatchdata,name="getbatchdata"),
    path('deletebatch/<int:id>',views.deletebatch,name="deletebatch"),
    path('searchbatch',views.searchbatch,name="searchbatch"),
    path('studentcredentials/<int:id>',views.studentcredentials,name="studentcredentials"),
    path('facultycredentials/<int:id>',views.facultycredentials,name="facultycredentials"),


    


    
    


    





    

    

    

    


    

    
    


    


    

    

    



    


    

    

    


    

    
    





      






   ]