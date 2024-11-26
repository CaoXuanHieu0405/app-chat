from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from users.models import CustomUser  # Import đúng model người dùng tùy chỉnh
from chat.models import Message, Room
from chat.serializers import MessageSerializer
from users.serializers import UserSerializer

class UserRegister(APIView):
    """
    API đăng ký người dùng mới
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class UserLogin(APIView):
    """
    API đăng nhập người dùng
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class SendMessage(APIView):
    """
    API gửi tin nhắn
    """
    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver')
        content = request.data.get('content', None)
        file = request.FILES.get('file', None)

        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Receiver does not exist'}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            file=file
        )
        return Response({
            "message": "Message sent successfully",
            "id": message.id,
        })

class ChatHistory(APIView):
    """
    API lấy lịch sử tin nhắn giữa hai người dùng
    """
    def get(self, request):
        sender_id = request.query_params.get('sender')
        receiver_id = request.query_params.get('receiver')

        if not sender_id or not receiver_id:
            return Response({'error': 'Sender and receiver IDs are required'}, status=status.HTTP_400_BAD_REQUEST)

        messages = Message.objects.filter(
            sender_id=sender_id,
            receiver_id=receiver_id
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class RoomChatHistory(APIView):
    """
    API lấy lịch sử tin nhắn trong phòng chat
    """
    def get(self, request, room_name):
        try:
            room = Room.objects.get(name=room_name)
            messages = Message.objects.filter(room=room).order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({'error': 'Room does not exist'}, status=status.HTTP_404_NOT_FOUND)