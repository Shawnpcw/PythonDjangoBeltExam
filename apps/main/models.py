from django.db import models
import bcrypt, re, datetime
class UserManager(models.Manager):
    def basic_validator(self, postData):
        result = {}
        errors = []
        
        EMAIL_REGEX = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b')
        
        Current_email = User.objects.filter(email=postData['email'])
        
        if len(postData['first_name']) <3:
            errors.append('First name should be at least 4 charaters!')
        if any(i.isdigit() for i in postData['first_name']):
            errors.append('First name should be only letters!')
        if len(postData['last_name']) <3:
            errors.append('Last name should be at least 4 charaters!')
        if any(i.isdigit() for i in postData['last_name']):
            errors.append('Last name should be only letters!')
        if len(postData['email']) <3:
            errors.append('Email should be at least 4 charaters!')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Enter a valid Email!')
        if len(Current_email)>0:
            errors.append('Email already exists!')
        if len(postData['password']) <7:
            errors.append('Password should be at least 8 charaters!')
        if postData['password'] != postData['pwcheck']:
            errors.append('Passwords dont match!')
        print(errors)

        if len(errors) ==0:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user =User.objects.create(first_name=postData['first_name'],last_name = postData['last_name'], email = postData['email'], pw_hash = hashed_pw.decode())
            result['user_id'] = new_user.id
        else:
            result['errors'] = errors
        return result
    def login_validator(self, postData):
        result = {}
        errors = []
        user = User.objects.filter(email=postData['email'])
        print('*'*50)
        if len(user) ==1:
            pw_hash = user[0].pw_hash
            print(pw_hash)
            if bcrypt.checkpw(postData['password'].encode(),pw_hash.encode()):
                print("password match")
                result['user_id'] = user[0].id
            else:
                print("failed password") 
                errors.append('Email or Password Incorrect')
                result['errors'] = errors
        else:
            errors.append('Email or Password Incorrect')
            print('failed retreving email') 
            result['errors'] = errors
        return result
class TripManager(models.Manager):
    def trip_validator(self, postData, userid):
        now = datetime.datetime.today().strftime('%Y-%m-%d')
        result = {}
        errors = []
        if postData['destination'] == '':
            errors.append('Destination entry cannot be blank!')
        if postData['description'] == '':
            errors.append('Description entry cannot be blank!')
        if postData['date_to'] == '':
            errors.append('Travel Date To entry cannot be blank!')
        if postData['date_from'] == '':
            errors.append('Travel Date From entry cannot be blank!')
        if postData['date_from'] > postData['date_to']:
            errors.append('Ending date must be greater than starting date!')
        if postData['date_from'] < now or postData['date_to'] < now:
            errors.append('Must start before today!')
        if len(errors) ==0:
            newtrip=Trip.objects.create(desc=postData['destination'], start_date=postData['date_from'], end_date=postData['date_to'], plan = postData['description'], trip_creater=User.objects.get(id= userid))
            
            User.objects.get(id=userid).your_trip.add(newtrip)
        else:
            result['errors'] = errors
        return result

class User(models.Model):
    first_name = models.CharField(max_length =255)
    last_name = models.CharField(max_length =255)
    email = models.CharField(max_length =255)
    pw_hash = models.CharField(max_length =255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    desc= models.CharField(max_length =255)
    start_date =models.DateField()
    end_date =models.DateField()
    plan =models.TextField(max_length=1000)
    trip_creater = models.ForeignKey(User, related_name='trip_created',on_delete=models.CASCADE)
    trip_attendee = models.ManyToManyField(User, related_name="your_trip")
    objects = TripManager()
