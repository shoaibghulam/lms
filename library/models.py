from django.db import models
from UniversityApp.models import UniversityAccount , UniversityBranch

CATEGORY=(
    ("digitallibrary","Digital Library"),
    ("digitallibraryphd","Digital Library Phd"),
)

# Create your models here.
class BookAuthor(models.Model):
    BookAuthorId=models.AutoField(primary_key=True)
    BookAuthorFirstName=models.CharField(max_length=100, default="First Name")
    BookAuthorLastName=models.CharField(max_length=100, default="Last Name")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.BookAuthorFirstName+"  "+ self.BookAuthorLastName
    


class Books(models.Model):
    BookId=models.AutoField(primary_key=True)
    BookTitle=models.CharField(max_length=240,default="Book Title")
    BookAuthorid=models.ForeignKey(BookAuthor,on_delete=models.CASCADE)
    BookEdition=models.CharField(max_length=10, default="0th")
    BookPublisher=models.CharField(max_length=150, default="Publisher")
    BookYearOfPublisher=models.DateField()
    BookISBN=models.CharField(max_length=100,default="Book ISBN")
    Bookcategory=models.CharField(max_length=40, choices=CATEGORY)
    BookFile= models.FileField(upload_to="Library/" ,default="book.pdf")
    BookCoverPage= models.ImageField(upload_to='Library/CoverPage', default="Cover Page")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.BookTitle 


        
    
    