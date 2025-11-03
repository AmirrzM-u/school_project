from rest_framework import serializers
from school.models import StudentAccount, ParentAccount, User, StudentTerm

class UserSerialier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'user_type']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number','user_type', 'password']
        # making passwords not to be shown to the users
        extra_kwargs = {
            'password': {'write_only': True}
        }   
    # overriding the create methode of the CreateAPIView to e able to create a user
    # when the serializer is running it runs a is_valid func to validate the data
    # and you can use the validation_data the use the data and create the user tith those data
    def create(self, validated_data):
        user = User(username=validated_data['username'], first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'], phone_number=validated_data['phone_number'],
                    user_type=validated_data['user_type'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class ParentAccountSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = ParentAccount
        fields = ['id', 'first_name', 'last_name']
    
    def get_first_name(self, instance):
        return instance.user.first_name
    def get_last_name(self, instance):
        return instance.user.last_name


class StudentAccountSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    # you can use other serializers data as this serializer data too
    student_parent = ParentAccountSerializer(read_only=True)
    # many=True means that it might have multiple objects and it would prevent upcoming errors

    class Meta:
        model = StudentAccount
        fields = ['id', 'id_student', 'first_name', 'last_name', 'grade_level', 'entry_year', 'student_parent', 'current_student']

    def get_first_name(self, instance):
        first_name = instance.user.first_name
        return first_name
    
    def get_last_name(self, instance):
        last_name = instance.user.last_name
        return last_name
    
class StudentTermSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    lesson_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    std_score = serializers.SerializerMethodField()

    class Meta:
        model = StudentTerm
        fields = ['student_name', 'lesson_name', 'teacher_name', 'std_score', 'term_year', 'active_term']

    def get_student_name(self, instance):
        student = instance.term_student
        return student.user.last_name
    def get_lesson_name(self, instance):
        lesson = instance.term_lesson
        return lesson.title
    def get_teacher_name(self, instance):
        teacher = instance.term_teacher
        return teacher.user.last_name
    def get_std_score(self, instance):
        if instance.student_score == 0:
            return 'no_score'
        else:
            return instance.student_score