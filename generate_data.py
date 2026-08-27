import json

# Stable, working Unsplash image URLs per topic keyword (no word-level lookup needed)
TOPIC_IMAGES = {
    "business":      "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&h=300&fit=crop",
    "travel":        "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&h=300&fit=crop",
    "daily":         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
    "university":    "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=400&h=300&fit=crop",
    "technology":    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=300&fit=crop",
    "sports":        "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400&h=300&fit=crop",
    "food":          "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop",
    "health":        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop",
    "shopping":      "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=300&fit=crop",
    "housing":       "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400&h=300&fit=crop",
    "weather":       "https://images.unsplash.com/photo-1504608524841-42584120d693?w=400&h=300&fit=crop",
    "entertainment": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400&h=300&fit=crop",
    "emotions":      "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&h=300&fit=crop",
}

topics = [
    {
        "id": "business",
        "name": "Business",
        "icon": "💼",
        "words": [
            { "word": "schedule", "meaning": "lịch trình", "phonetic": "/ˈskedʒ.uːl/", "example": "We need to change the meeting schedule.", "example_vi": "Chúng ta cần thay đổi lịch họp.", "topic": "Business" },
            { "word": "deadline", "meaning": "hạn chót", "phonetic": "/ˈded.laɪn/", "example": "The deadline for the report is Friday.", "example_vi": "Hạn nộp báo cáo là thứ Sáu.", "topic": "Business" },
            { "word": "negotiate", "meaning": "thương lượng", "phonetic": "/nəˈɡoʊ.ʃi.eɪt/", "example": "We need to negotiate a better price.", "example_vi": "Chúng ta cần thương lượng một mức giá tốt hơn.", "topic": "Business" }
        ]
    },
    {
        "id": "travel",
        "name": "Travel",
        "icon": "✈️",
        "words": [
            { "word": "boarding pass", "meaning": "thẻ lên máy bay", "phonetic": "/ˈbɔːr.dɪŋ pæs/", "example": "Please show your boarding pass at the gate.", "example_vi": "Vui lòng xuất trình thẻ lên máy bay tại cổng.", "topic": "Travel" },
            { "word": "reservation", "meaning": "đặt chỗ", "phonetic": "/ˌrez.ɚˈveɪ.ʃən/", "example": "I made a reservation for two people.", "example_vi": "Tôi đã đặt chỗ cho hai người.", "topic": "Travel" }
        ]
    },
    {
        "id": "daily",
        "name": "Daily life",
        "icon": "☀️",
        "words": [
            { "word": "appointment", "meaning": "cuộc hẹn", "phonetic": "/əˈpɔɪnt.mənt/", "example": "She has a dentist appointment tomorrow.", "example_vi": "Cô ấy có lịch hẹn nha sĩ vào ngày mai.", "topic": "Daily life" }
        ]
    }
]

new_topics_data = [
    {
        "id": "university",
        "name": "University & Studies",
        "icon": "🎓",
        "words": [
            {"word": "assignment", "meaning": "bài tập", "phonetic": "/əˈsaɪn.mənt/", "example": "I have a lot of assignments to do this weekend.", "example_vi": "Tôi có rất nhiều bài tập phải làm cuối tuần này."},
            {"word": "lecture", "meaning": "bài giảng", "phonetic": "/ˈlek.tʃɚ/", "example": "The lecture was about ancient history.", "example_vi": "Bài giảng nói về lịch sử cổ đại."},
            {"word": "scholarship", "meaning": "học bổng", "phonetic": "/ˈskɑː.lɚ.ʃɪp/", "example": "She won a scholarship to study abroad.", "example_vi": "Cô ấy đã giành được học bổng để học ở nước ngoài."},
            {"word": "curriculum", "meaning": "chương trình học", "phonetic": "/kəˈrɪk.jə.ləm/", "example": "Math is an important part of the school curriculum.", "example_vi": "Toán học là một phần quan trọng của chương trình học."},
            {"word": "campus", "meaning": "khuôn viên trường", "phonetic": "/ˈkæm.pəs/", "example": "We walked around the university campus.", "example_vi": "Chúng tôi đi dạo quanh khuôn viên trường đại học."},
            {"word": "semester", "meaning": "học kỳ", "phonetic": "/səˈmes.tɚ/", "example": "The first semester ends in December.", "example_vi": "Học kỳ đầu tiên kết thúc vào tháng Mười Hai."},
            {"word": "thesis", "meaning": "luận văn", "phonetic": "/ˈθiː.sɪs/", "example": "He is writing a thesis on climate change.", "example_vi": "Anh ấy đang viết luận văn về biến đổi khí hậu."},
            {"word": "graduate", "meaning": "tốt nghiệp", "phonetic": "/ˈɡrædʒ.u.ət/", "example": "She will graduate next year.", "example_vi": "Cô ấy sẽ tốt nghiệp vào năm tới."},
            {"word": "tuition", "meaning": "học phí", "phonetic": "/tuːˈɪʃ.ən/", "example": "Tuition fees have increased again.", "example_vi": "Học phí đã tăng lần nữa."},
            {"word": "professor", "meaning": "giáo sư", "phonetic": "/prəˈfes.ɚ/", "example": "The professor answered my question clearly.", "example_vi": "Giáo sư đã trả lời câu hỏi của tôi rõ ràng."},
            {"word": "dormitory", "meaning": "ký túc xá", "phonetic": "/ˈdɔːr.mə.tɔːr.i/", "example": "Students usually live in a dormitory.", "example_vi": "Sinh viên thường sống trong ký túc xá."},
            {"word": "enroll", "meaning": "nhập học, đăng ký", "phonetic": "/ɪnˈroʊl/", "example": "You need to enroll before September.", "example_vi": "Bạn cần phải đăng ký trước tháng Chín."},
            {"word": "faculty", "meaning": "khoa (trường ĐH)", "phonetic": "/ˈfæk.əl.t̬i/", "example": "He is a member of the science faculty.", "example_vi": "Anh ấy là thành viên của khoa khoa học."},
            {"word": "syllabus", "meaning": "đề cương môn học", "phonetic": "/ˈsɪl.ə.bəs/", "example": "The teacher gave us a copy of the syllabus.", "example_vi": "Giáo viên đã cho chúng tôi một bản đề cương."},
            {"word": "major", "meaning": "chuyên ngành", "phonetic": "/ˈmeɪ.dʒɚ/", "example": "My major is computer science.", "example_vi": "Chuyên ngành của tôi là khoa học máy tính."},
            {"word": "degree", "meaning": "bằng cấp", "phonetic": "/dɪˈɡriː/", "example": "She has a master's degree in biology.", "example_vi": "Cô ấy có bằng thạc sĩ về sinh học."},
            {"word": "undergraduate", "meaning": "sinh viên chưa tốt nghiệp", "phonetic": "/ˌʌn.dɚˈɡrædʒ.u.ət/", "example": "This course is for undergraduate students.", "example_vi": "Khóa học này dành cho sinh viên chưa tốt nghiệp."},
            {"word": "postgraduate", "meaning": "sau đại học", "phonetic": "/ˌpoʊstˈɡrædʒ.u.ət/", "example": "He is doing postgraduate research.", "example_vi": "Anh ấy đang thực hiện nghiên cứu sau đại học."},
            {"word": "academic", "meaning": "thuộc học thuật", "phonetic": "/ˌæk.əˈdem.ɪk/", "example": "She has an excellent academic record.", "example_vi": "Cô ấy có thành tích học tập xuất sắc."},
            {"word": "research", "meaning": "nghiên cứu", "phonetic": "/ˈriː.sɝːtʃ/", "example": "They are doing research on a new drug.", "example_vi": "Họ đang nghiên cứu về một loại thuốc mới."},
            {"word": "presentation", "meaning": "bài thuyết trình", "phonetic": "/ˌprez.ənˈteɪ.ʃən/", "example": "I have to give a presentation tomorrow.", "example_vi": "Tôi phải thuyết trình vào ngày mai."},
            {"word": "seminar", "meaning": "hội thảo", "phonetic": "/ˈsem.ə.nɑːr/", "example": "I attended a seminar on modern art.", "example_vi": "Tôi đã tham dự một hội thảo về nghệ thuật hiện đại."},
            {"word": "credit", "meaning": "tín chỉ", "phonetic": "/ˈkred.ɪt/", "example": "This class is worth three credits.", "example_vi": "Lớp học này có giá trị ba tín chỉ."},
            {"word": "alumni", "meaning": "cựu sinh viên", "phonetic": "/əˈlʌm.naɪ/", "example": "The university has a strong alumni network.", "example_vi": "Trường đại học có mạng lưới cựu sinh viên vững mạnh."},
            {"word": "cram", "meaning": "nhồi nhét (học)", "phonetic": "/kræm/", "example": "I had to cram for the exam last night.", "example_vi": "Tôi phải học nhồi cho kỳ thi vào tối qua."},
            {"word": "plagiarism", "meaning": "đạo văn", "phonetic": "/ˈpleɪ.dʒə.rɪ.zəm/", "example": "Plagiarism is a serious offense in college.", "example_vi": "Đạo văn là hành vi vi phạm nghiêm trọng ở đại học."},
            {"word": "tutor", "meaning": "gia sư", "phonetic": "/ˈtuː.t̬ɚ/", "example": "His parents hired a tutor to help him with math.", "example_vi": "Bố mẹ anh ấy thuê gia sư để giúp anh ấy học toán."},
            {"word": "exam", "meaning": "kỳ thi", "phonetic": "/ɪɡˈzæm/", "example": "I failed the final exam.", "example_vi": "Tôi đã trượt kỳ thi cuối kỳ."},
            {"word": "grade", "meaning": "điểm số", "phonetic": "/ɡreɪd/", "example": "She always gets good grades.", "example_vi": "Cô ấy luôn đạt điểm tốt."},
            {"word": "review", "meaning": "ôn tập", "phonetic": "/rɪˈvjuː/", "example": "Let's review Chapter 5 before the test.", "example_vi": "Hãy ôn lại chương 5 trước khi kiểm tra."}
        ]
    },
    {
        "id": "technology",
        "name": "Technology & Networks",
        "icon": "💻",
        "words": [
            {"word": "database", "meaning": "cơ sở dữ liệu", "phonetic": "/ˈdeɪ.t̬ə.beɪs/", "example": "The customer information is stored in a database.", "example_vi": "Thông tin khách hàng được lưu trữ trong cơ sở dữ liệu."},
            {"word": "network", "meaning": "mạng lưới", "phonetic": "/ˈnet.wɝːk/", "example": "The computer network is down today.", "example_vi": "Mạng máy tính hôm nay bị lỗi."},
            {"word": "algorithm", "meaning": "thuật toán", "phonetic": "/ˈæl.ɡə.rɪ.ðəm/", "example": "Google uses a complex search algorithm.", "example_vi": "Google sử dụng một thuật toán tìm kiếm phức tạp."},
            {"word": "encryption", "meaning": "mã hóa", "phonetic": "/ɪnˈkrɪp.ʃən/", "example": "End-to-end encryption keeps messages secure.", "example_vi": "Mã hóa đầu cuối giữ cho tin nhắn được bảo mật."},
            {"word": "server", "meaning": "máy chủ", "phonetic": "/ˈsɝː.vɚ/", "example": "The website is hosted on a private server.", "example_vi": "Trang web được lưu trữ trên một máy chủ riêng."},
            {"word": "hardware", "meaning": "phần cứng", "phonetic": "/ˈhɑːrd.wer/", "example": "We need to upgrade the computer hardware.", "example_vi": "Chúng ta cần nâng cấp phần cứng máy tính."},
            {"word": "software", "meaning": "phần mềm", "phonetic": "/ˈsɑːft.wer/", "example": "Please install the latest software update.", "example_vi": "Vui lòng cài đặt bản cập nhật phần mềm mới nhất."},
            {"word": "bandwidth", "meaning": "băng thông", "phonetic": "/ˈbænd.wɪdtθ/", "example": "Downloading huge files takes a lot of bandwidth.", "example_vi": "Tải xuống các tệp lớn đòi hỏi nhiều băng thông."},
            {"word": "firewall", "meaning": "tường lửa", "phonetic": "/ˈfaɪr.wɑːl/", "example": "The company uses a firewall to prevent hacking.", "example_vi": "Công ty sử dụng tường lửa để ngăn chặn tấn công mạng."},
            {"word": "cybersecurity", "meaning": "an ninh mạng", "phonetic": "/ˌsaɪ.bɚ.səˈkjʊr.ə.t̬i/", "example": "Cybersecurity is important for online banking.", "example_vi": "An ninh mạng rất quan trọng đối với ngân hàng trực tuyến."},
            {"word": "cloud", "meaning": "đám mây (lưu trữ)", "phonetic": "/klaʊd/", "example": "I saved all my photos in the cloud.", "example_vi": "Tôi đã lưu tất cả ảnh của mình trên đám mây."},
            {"word": "interface", "meaning": "giao diện", "phonetic": "/ˈɪn.t̬ɚ.feɪs/", "example": "The app has a very user-friendly interface.", "example_vi": "Ứng dụng có giao diện rất thân thiện với người dùng."},
            {"word": "virtual", "meaning": "ảo", "phonetic": "/ˈvɝː.tʃu.əl/", "example": "Virtual reality is changing the gaming industry.", "example_vi": "Thực tế ảo đang thay đổi ngành công nghiệp game."},
            {"word": "wireless", "meaning": "không dây", "phonetic": "/ˈwaɪr.ləs/", "example": "My laptop connects to a wireless network.", "example_vi": "Máy tính xách tay của tôi kết nối với mạng không dây."},
            {"word": "browser", "meaning": "trình duyệt", "phonetic": "/ˈbraʊ.zɚ/", "example": "Which web browser do you use?", "example_vi": "Bạn dùng trình duyệt web nào?"},
            {"word": "application", "meaning": "ứng dụng", "phonetic": "/ˌæp.ləˈkeɪ.ʃən/", "example": "I downloaded a new fitness application.", "example_vi": "Tôi đã tải xuống một ứng dụng thể dục mới."},
            {"word": "innovative", "meaning": "đổi mới, sáng tạo", "phonetic": "/ˈɪn.ə.veɪ.t̬ɪv/", "example": "Apple is known for innovative products.", "example_vi": "Apple được biết đến với các sản phẩm sáng tạo."},
            {"word": "automate", "meaning": "tự động hóa", "phonetic": "/ˈɑː.t̬ə.meɪt/", "example": "They want to automate the production process.", "example_vi": "Họ muốn tự động hóa quy trình sản xuất."},
            {"word": "glitch", "meaning": "lỗi kỹ thuật nhỏ", "phonetic": "/ɡlɪtʃ/", "example": "The system crashed due to a software glitch.", "example_vi": "Hệ thống bị sập do lỗi phần mềm."},
            {"word": "upgrade", "meaning": "nâng cấp", "phonetic": "/ˈʌp.ɡreɪd/", "example": "It's time to upgrade my phone.", "example_vi": "Đã đến lúc nâng cấp điện thoại của tôi."},
            {"word": "compatible", "meaning": "tương thích", "phonetic": "/kəmˈpæt̬.ə.bəl/", "example": "This software is not compatible with Windows.", "example_vi": "Phần mềm này không tương thích với Windows."},
            {"word": "gadget", "meaning": "thiết bị điện tử", "phonetic": "/ˈɡædʒ.ət/", "example": "He loves buying new electronic gadgets.", "example_vi": "Anh ấy thích mua các thiết bị điện tử mới."},
            {"word": "reboot", "meaning": "khởi động lại", "phonetic": "/ˌriːˈbuːt/", "example": "Try to reboot your computer.", "example_vi": "Hãy thử khởi động lại máy tính của bạn."},
            {"word": "download", "meaning": "tải xuống", "phonetic": "/ˈdaʊn.loʊd/", "example": "You can download the file from our website.", "example_vi": "Bạn có thể tải tệp từ trang web của chúng tôi."},
            {"word": "upload", "meaning": "tải lên", "phonetic": "/ˈʌp.loʊd/", "example": "It takes time to upload a large video.", "example_vi": "Mất thời gian để tải lên một video lớn."},
            {"word": "install", "meaning": "cài đặt", "phonetic": "/ɪnˈstɑːl/", "example": "Click here to install the program.", "example_vi": "Nhấp vào đây để cài đặt chương trình."},
            {"word": "delete", "meaning": "xóa", "phonetic": "/dɪˈliːt/", "example": "Don't delete that folder!", "example_vi": "Đừng xóa thư mục đó!"},
            {"word": "password", "meaning": "mật khẩu", "phonetic": "/ˈpæs.wɝːd/", "example": "Choose a strong password for your account.", "example_vi": "Hãy chọn một mật khẩu mạnh cho tài khoản của bạn."},
            {"word": "username", "meaning": "tên người dùng", "phonetic": "/ˈjuː.zɚ.neɪm/", "example": "Please enter your username and password.", "example_vi": "Vui lòng nhập tên người dùng và mật khẩu của bạn."},
            {"word": "digital", "meaning": "kỹ thuật số", "phonetic": "/ˈdɪdʒ.ə.t̬əl/", "example": "Digital marketing is growing rapidly.", "example_vi": "Tiếp thị kỹ thuật số đang phát triển nhanh chóng."}
        ]
    },
    {
        "id": "sports",
        "name": "Football & Sports",
        "icon": "⚽",
        "words": [
            {"word": "stadium", "meaning": "sân vận động", "phonetic": "/ˈsteɪ.di.əm/", "example": "The stadium was full of fans.", "example_vi": "Sân vận động chật ních fan hâm mộ."},
            {"word": "tournament", "meaning": "giải đấu", "phonetic": "/ˈtʊr.nə.mənt/", "example": "Our team won the local tennis tournament.", "example_vi": "Đội của chúng tôi đã giành chiến thắng trong giải tennis địa phương."},
            {"word": "referee", "meaning": "trọng tài", "phonetic": "/ˌref.əˈriː/", "example": "The referee blew the whistle to end the game.", "example_vi": "Trọng tài thổi còi kết thúc trận đấu."},
            {"word": "coach", "meaning": "huấn luyện viên", "phonetic": "/koʊtʃ/", "example": "The coach gave them a pep talk.", "example_vi": "Huấn luyện viên đã động viên họ."},
            {"word": "athlete", "meaning": "vận động viên", "phonetic": "/ˈæθ.liːt/", "example": "She is a professional athlete.", "example_vi": "Cô ấy là một vận động viên chuyên nghiệp."},
            {"word": "champion", "meaning": "nhà vô địch", "phonetic": "/ˈtʃæm.pi.ən/", "example": "They are the world champions.", "example_vi": "Họ là nhà vô địch thế giới."},
            {"word": "medal", "meaning": "huy chương", "phonetic": "/ˈmed.əl/", "example": "He won a gold medal in swimming.", "example_vi": "Anh ấy giành được huy chương vàng môn bơi lội."},
            {"word": "penalty", "meaning": "phạt đền", "phonetic": "/ˈpen.əl.ti/", "example": "The team was awarded a penalty kick.", "example_vi": "Đội được trao một quả phạt đền."},
            {"word": "substitute", "meaning": "cầu thủ dự bị", "phonetic": "/ˈsʌb.stə.tuːt/", "example": "The manager sent in a substitute player.", "example_vi": "HLV đưa cầu thủ dự bị vào sân."},
            {"word": "defense", "meaning": "phòng thủ", "phonetic": "/dɪˈfens/", "example": "Their defense was very strong today.", "example_vi": "Hàng phòng thủ của họ rất mạnh hôm nay."},
            {"word": "offense", "meaning": "tấn công", "phonetic": "/əˈfens/", "example": "The team needs to improve its offense.", "example_vi": "Đội cần cải thiện khả năng tấn công."},
            {"word": "tactics", "meaning": "chiến thuật", "phonetic": "/ˈtæk.tɪks/", "example": "They discussed their tactics before the match.", "example_vi": "Họ thảo luận về chiến thuật trước trận đấu."},
            {"word": "captain", "meaning": "đội trưởng", "phonetic": "/ˈkæp.tɪn/", "example": "He is the captain of the football team.", "example_vi": "Anh ấy là đội trưởng của đội bóng đá."},
            {"word": "goalkeeper", "meaning": "thủ môn", "phonetic": "/ˈɡoʊlˌkiː.pɚ/", "example": "The goalkeeper made a great save.", "example_vi": "Thủ môn đã thực hiện một pha cứu thua tuyệt vời."},
            {"word": "foul", "meaning": "phạm lỗi", "phonetic": "/faʊl/", "example": "He committed a foul near the penalty area.", "example_vi": "Anh ta phạm lỗi gần khu vực phạt đền."},
            {"word": "whistle", "meaning": "cái còi", "phonetic": "/ˈwɪs.əl/", "example": "The referee blew the whistle.", "example_vi": "Trọng tài thổi còi."},
            {"word": "trophy", "meaning": "cúp", "phonetic": "/ˈtroʊ.fi/", "example": "They lifted the trophy in celebration.", "example_vi": "Họ nâng cao chiếc cúp để ăn mừng."},
            {"word": "score", "meaning": "ghi bàn, tỉ số", "phonetic": "/skɔːr/", "example": "What is the final score?", "example_vi": "Tỉ số cuối cùng là bao nhiêu?"},
            {"word": "match", "meaning": "trận đấu", "phonetic": "/mætʃ/", "example": "I watched the match on TV.", "example_vi": "Tôi xem trận đấu trên TV."},
            {"word": "opponent", "meaning": "đối thủ", "phonetic": "/əˈpoʊ.nənt/", "example": "He beat his opponent easily.", "example_vi": "Anh ta đã đánh bại đối thủ của mình một cách dễ dàng."},
            {"word": "league", "meaning": "giải đấu (câu lạc bộ)", "phonetic": "/liːɡ/", "example": "Manchester City won the Premier League.", "example_vi": "Manchester City đã vô địch Premier League."},
            {"word": "fitness", "meaning": "thể lực", "phonetic": "/ˈfɪt.nəs/", "example": "Players need a high level of fitness.", "example_vi": "Cầu thủ cần có thể lực tốt."},
            {"word": "injury", "meaning": "chấn thương", "phonetic": "/ˈɪn.dʒər.i/", "example": "He suffered a knee injury.", "example_vi": "Anh ấy bị chấn thương đầu gối."},
            {"word": "cheer", "meaning": "cổ vũ", "phonetic": "/tʃɪr/", "example": "The fans cheered for their team.", "example_vi": "Các fan hâm mộ cổ vũ cho đội của họ."},
            {"word": "victory", "meaning": "chiến thắng", "phonetic": "/ˈvɪk.tɚ.i/", "example": "It was a great victory for the club.", "example_vi": "Đó là một chiến thắng vĩ đại cho câu lạc bộ."},
            {"word": "defeat", "meaning": "thất bại", "phonetic": "/dɪˈfiːt/", "example": "The team accepted their defeat gracefully.", "example_vi": "Đội chấp nhận thất bại một cách lịch sự."},
            {"word": "draw", "meaning": "hòa", "phonetic": "/drɑː/", "example": "The match ended in a 1-1 draw.", "example_vi": "Trận đấu kết thúc với tỉ số hòa 1-1."},
            {"word": "compete", "meaning": "cạnh tranh, thi đấu", "phonetic": "/kəmˈpiːt/", "example": "Athletes from all over the world will compete.", "example_vi": "Vận động viên từ khắp nơi trên thế giới sẽ tranh tài."},
            {"word": "spectator", "meaning": "khán giả (ngoài trời)", "phonetic": "/ˈspek.teɪ.t̬ɚ/", "example": "Thousands of spectators watched the game.", "example_vi": "Hàng ngàn khán giả đã theo dõi trận đấu."},
            {"word": "pitch", "meaning": "sân cỏ", "phonetic": "/pɪtʃ/", "example": "The players walked onto the pitch.", "example_vi": "Các cầu thủ bước ra sân cỏ."}
        ]
    },
    {
        "id": "food",
        "name": "Food & Cooking",
        "icon": "🍔",
        "words": [
            {"word": "ingredient", "meaning": "thành phần, nguyên liệu", "phonetic": "/ɪnˈɡriː.di.ənt/", "example": "I have all the ingredients to bake a cake.", "example_vi": "Tôi có đủ nguyên liệu để làm bánh."},
            {"word": "recipe", "meaning": "công thức nấu ăn", "phonetic": "/ˈres.ə.pi/", "example": "Could you give me the recipe for this soup?", "example_vi": "Bạn có thể cho tôi công thức nấu món súp này không?"},
            {"word": "appetizer", "meaning": "món khai vị", "phonetic": "/ˈæp.ə.taɪ.zɚ/", "example": "We ordered a salad as an appetizer.", "example_vi": "Chúng tôi gọi salad làm món khai vị."},
            {"word": "dessert", "meaning": "món tráng miệng", "phonetic": "/dɪˈzɝːt/", "example": "I'd like ice cream for dessert.", "example_vi": "Tôi muốn ăn kem tráng miệng."},
            {"word": "beverage", "meaning": "đồ uống", "phonetic": "/ˈbev.ɚ.ɪdʒ/", "example": "Hot beverages are served in the cafe.", "example_vi": "Đồ uống nóng được phục vụ trong quán cà phê."},
            {"word": "nutrition", "meaning": "dinh dưỡng", "phonetic": "/nuːˈtrɪʃ.ən/", "example": "Good nutrition is essential for health.", "example_vi": "Dinh dưỡng tốt là điều cần thiết cho sức khỏe."},
            {"word": "flavor", "meaning": "hương vị", "phonetic": "/ˈfleɪ.vɚ/", "example": "This soup has a very spicy flavor.", "example_vi": "Món súp này có hương vị rất cay."},
            {"word": "vegetarian", "meaning": "người ăn chay", "phonetic": "/ˌvedʒ.əˈter.i.ən/", "example": "My sister is a vegetarian.", "example_vi": "Chị gái tôi ăn chay."},
            {"word": "seasoning", "meaning": "gia vị", "phonetic": "/ˈsiː.zən.ɪŋ/", "example": "Add some seasoning to the meat.", "example_vi": "Thêm gia vị vào thịt."},
            {"word": "bake", "meaning": "nướng (bằng lò)", "phonetic": "/beɪk/", "example": "I am going to bake a cake for her birthday.", "example_vi": "Tôi sẽ nướng bánh cho sinh nhật của cô ấy."},
            {"word": "fry", "meaning": "chiên, rán", "phonetic": "/fraɪ/", "example": "Fry the potatoes until they are golden brown.", "example_vi": "Chiên khoai tây cho đến khi vàng đều."},
            {"word": "boil", "meaning": "luộc, đun sôi", "phonetic": "/bɔɪl/", "example": "Boil the water before adding the noodles.", "example_vi": "Đun sôi nước trước khi cho mì vào."},
            {"word": "grill", "meaning": "nướng (trên vỉ)", "phonetic": "/ɡrɪl/", "example": "We had grilled chicken for dinner.", "example_vi": "Chúng tôi ăn thịt gà nướng vỉ cho bữa tối."},
            {"word": "roast", "meaning": "quay, nướng (thịt)", "phonetic": "/roʊst/", "example": "I am roasting a duck for dinner.", "example_vi": "Tôi đang quay một con vịt cho bữa tối."},
            {"word": "chop", "meaning": "thái, băm", "phonetic": "/tʃɑːp/", "example": "Chop the onions finely.", "example_vi": "Băm nhỏ hành tây."},
            {"word": "slice", "meaning": "thái lát", "phonetic": "/slaɪs/", "example": "Slice the tomatoes and put them in the salad.", "example_vi": "Thái lát cà chua và cho vào salad."},
            {"word": "stir", "meaning": "khuấy", "phonetic": "/stɝː/", "example": "Stir the soup slowly.", "example_vi": "Khuấy súp từ từ."},
            {"word": "blend", "meaning": "xay, trộn", "phonetic": "/blend/", "example": "Blend the fruits to make a smoothie.", "example_vi": "Xay trái cây để làm sinh tố."},
            {"word": "taste", "meaning": "nếm", "phonetic": "/teɪst/", "example": "Taste the sauce and add salt if needed.", "example_vi": "Nếm thử nước sốt và thêm muối nếu cần."},
            {"word": "sour", "meaning": "chua", "phonetic": "/saʊr/", "example": "These lemons are very sour.", "example_vi": "Những quả chanh này rất chua."},
            {"word": "bitter", "meaning": "đắng", "phonetic": "/ˈbɪt̬.ɚ/", "example": "Black coffee is often bitter.", "example_vi": "Cà phê đen thường có vị đắng."},
            {"word": "spicy", "meaning": "cay", "phonetic": "/ˈspaɪ.si/", "example": "I love eating spicy food.", "example_vi": "Tôi thích ăn đồ cay."},
            {"word": "salty", "meaning": "mặn", "phonetic": "/ˈsɑːl.t̬i/", "example": "This soup is too salty.", "example_vi": "Món súp này quá mặn."},
            {"word": "sweet", "meaning": "ngọt", "phonetic": "/swiːt/", "example": "She likes sweet desserts.", "example_vi": "Cô ấy thích món tráng miệng ngọt."},
            {"word": "fresh", "meaning": "tươi", "phonetic": "/freʃ/", "example": "Buy some fresh vegetables from the market.", "example_vi": "Mua rau tươi từ chợ."},
            {"word": "raw", "meaning": "sống (chưa nấu)", "phonetic": "/rɑː/", "example": "Sushi is made with raw fish.", "example_vi": "Sushi được làm từ cá sống."},
            {"word": "chef", "meaning": "đầu bếp", "phonetic": "/ʃef/", "example": "The chef prepared a special dish.", "example_vi": "Đầu bếp đã chuẩn bị một món đặc biệt."},
            {"word": "menu", "meaning": "thực đơn", "phonetic": "/ˈmen.juː/", "example": "Can I see the menu, please?", "example_vi": "Cho tôi xem thực đơn được không?"},
            {"word": "order", "meaning": "đặt món", "phonetic": "/ˈɔːr.dɚ/", "example": "Are you ready to order?", "example_vi": "Bạn đã sẵn sàng gọi món chưa?"},
            {"word": "delicious", "meaning": "ngon miệng", "phonetic": "/dɪˈlɪʃ.əs/", "example": "The meal was absolutely delicious.", "example_vi": "Bữa ăn thực sự rất ngon miệng."}
        ]
    },
    {
        "id": "health",
        "name": "Health & Fitness",
        "icon": "💪",
        "words": [
            {"word": "exercise", "meaning": "tập thể dục", "phonetic": "/ˈek.sɚ.saɪz/", "example": "You should exercise daily to stay fit.", "example_vi": "Bạn nên tập thể dục hàng ngày để giữ sức khỏe."},
            {"word": "muscle", "meaning": "cơ bắp", "phonetic": "/ˈmʌs.əl/", "example": "Lifting weights builds muscle.", "example_vi": "Tập tạ giúp xây dựng cơ bắp."},
            {"word": "cardio", "meaning": "bài tập tim mạch", "phonetic": "/ˈkɑːr.di.oʊ/", "example": "Running and swimming are good cardio exercises.", "example_vi": "Chạy bộ và bơi lội là bài tập tim mạch tốt."},
            {"word": "diet", "meaning": "chế độ ăn kiêng", "phonetic": "/ˈdaɪ.ət/", "example": "She is on a strict diet to lose weight.", "example_vi": "Cô ấy đang theo chế độ ăn kiêng nghiêm ngặt để giảm cân."},
            {"word": "vitamin", "meaning": "vi-ta-min", "phonetic": "/ˈvaɪ.t̬ə.mɪn/", "example": "Oranges are a great source of vitamin C.", "example_vi": "Cam là nguồn cung cấp vitamin C tuyệt vời."},
            {"word": "symptom", "meaning": "triệu chứng", "phonetic": "/ˈsɪmp.təm/", "example": "A fever is a common symptom of the flu.", "example_vi": "Sốt là triệu chứng phổ biến của cúm."},
            {"word": "disease", "meaning": "bệnh tật", "phonetic": "/dɪˈziːz/", "example": "Heart disease is a major cause of death.", "example_vi": "Bệnh tim là nguyên nhân gây tử vong chính."},
            {"word": "treatment", "meaning": "điều trị", "phonetic": "/ˈtriːt.mənt/", "example": "He is receiving treatment for cancer.", "example_vi": "Anh ấy đang được điều trị ung thư."},
            {"word": "surgery", "meaning": "phẫu thuật", "phonetic": "/ˈsɝː.dʒɚ.i/", "example": "She had to undergo knee surgery.", "example_vi": "Cô ấy phải phẫu thuật đầu gối."},
            {"word": "medicine", "meaning": "thuốc", "phonetic": "/ˈmed.ɪ.sən/", "example": "Did you take your medicine today?", "example_vi": "Hôm nay bạn đã uống thuốc chưa?"},
            {"word": "prescription", "meaning": "đơn thuốc", "phonetic": "/prɪˈskrɪp.ʃən/", "example": "The doctor wrote a prescription for antibiotics.", "example_vi": "Bác sĩ đã kê đơn thuốc kháng sinh."},
            {"word": "therapy", "meaning": "liệu pháp", "phonetic": "/ˈθer.ə.pi/", "example": "Physical therapy helped him recover.", "example_vi": "Vật lý trị liệu đã giúp anh ấy hồi phục."},
            {"word": "clinic", "meaning": "phòng khám", "phonetic": "/ˈklɪn.ɪk/", "example": "I need to visit the dental clinic.", "example_vi": "Tôi cần đến phòng khám nha khoa."},
            {"word": "patient", "meaning": "bệnh nhân", "phonetic": "/ˈpeɪ.ʃənt/", "example": "The hospital is full of patients.", "example_vi": "Bệnh viện chật ních bệnh nhân."},
            {"word": "recovery", "meaning": "sự phục hồi", "phonetic": "/rɪˈkʌv.ɚ.i/", "example": "He made a full recovery after the accident.", "example_vi": "Anh ấy đã hồi phục hoàn toàn sau tai nạn."},
            {"word": "obesity", "meaning": "béo phì", "phonetic": "/oʊˈbiː.sə.t̬i/", "example": "Obesity is a growing problem in many countries.", "example_vi": "Béo phì là vấn đề ngày càng tăng ở nhiều quốc gia."},
            {"word": "immune", "meaning": "miễn dịch", "phonetic": "/ɪˈmjuːn/", "example": "A healthy diet boosts your immune system.", "example_vi": "Chế độ ăn lành mạnh tăng cường hệ miễn dịch."},
            {"word": "vaccine", "meaning": "vắc-xin", "phonetic": "/ˈvæk.siːn/", "example": "Researchers have developed a new vaccine.", "example_vi": "Các nhà nghiên cứu đã phát triển một loại vắc-xin mới."},
            {"word": "stress", "meaning": "căng thẳng", "phonetic": "/stres/", "example": "Yoga can help reduce stress.", "example_vi": "Yoga có thể giúp giảm căng thẳng."},
            {"word": "mental", "meaning": "thuộc tinh thần", "phonetic": "/ˈmen.təl/", "example": "Mental health is just as important as physical health.", "example_vi": "Sức khỏe tinh thần quan trọng không kém sức khỏe thể chất."},
            {"word": "hygiene", "meaning": "vệ sinh", "phonetic": "/ˈhaɪ.dʒiːn/", "example": "Good dental hygiene prevents tooth decay.", "example_vi": "Vệ sinh răng miệng tốt giúp ngăn ngừa sâu răng."},
            {"word": "allergy", "meaning": "dị ứng", "phonetic": "/ˈæl.ɚ.dʒi/", "example": "I have a severe allergy to peanuts.", "example_vi": "Tôi bị dị ứng nặng với lạc."},
            {"word": "blood", "meaning": "máu", "phonetic": "/blʌd/", "example": "He donated blood at the hospital.", "example_vi": "Anh ấy đã hiến máu tại bệnh viện."},
            {"word": "bone", "meaning": "xương", "phonetic": "/boʊn/", "example": "He broke a bone in his leg.", "example_vi": "Anh ấy đã gãy xương ở chân."},
            {"word": "breathe", "meaning": "thở", "phonetic": "/briːð/", "example": "It's hard to breathe at high altitudes.", "example_vi": "Rất khó thở ở độ cao lớn."},
            {"word": "cough", "meaning": "ho", "phonetic": "/kɑːf/", "example": "Cover your mouth when you cough.", "example_vi": "Che miệng khi ho."},
            {"word": "fever", "meaning": "sốt", "phonetic": "/ˈfiː.vɚ/", "example": "The baby has a high fever.", "example_vi": "Em bé bị sốt cao."},
            {"word": "headache", "meaning": "đau đầu", "phonetic": "/ˈhed.eɪk/", "example": "I have a terrible headache today.", "example_vi": "Hôm nay tôi bị đau đầu dữ dội."},
            {"word": "pain", "meaning": "đau đớn", "phonetic": "/peɪn/", "example": "Are you experiencing any pain in your back?", "example_vi": "Bạn có bị đau lưng không?"},
            {"word": "healthy", "meaning": "khỏe mạnh", "phonetic": "/ˈhel.θi/", "example": "I try to eat a healthy diet.", "example_vi": "Tôi cố gắng ăn uống lành mạnh."}
        ]
    },
    {
        "id": "shopping",
        "name": "Shopping & Fashion",
        "icon": "🛍️",
        "words": [
            {"word": "discount", "meaning": "giảm giá", "phonetic": "/ˈdɪs.kaʊnt/", "example": "They are offering a 20% discount today.", "example_vi": "Họ đang giảm giá 20% hôm nay."},
            {"word": "bargain", "meaning": "mặc cả, món hời", "phonetic": "/ˈbɑːr.ɡɪn/", "example": "This shirt was a real bargain.", "example_vi": "Chiếc áo này thực sự là một món hời."},
            {"word": "receipt", "meaning": "biên lai", "phonetic": "/rɪˈsiːt/", "example": "Keep your receipt in case you want to return it.", "example_vi": "Giữ biên lai phòng khi bạn muốn trả lại."},
            {"word": "refund", "meaning": "hoàn tiền", "phonetic": "/ˈriː.fʌnd/", "example": "Can I get a refund if it doesn't fit?", "example_vi": "Tôi có thể được hoàn tiền nếu không vừa không?"},
            {"word": "cashier", "meaning": "thu ngân", "phonetic": "/kæʃˈɪr/", "example": "The cashier will scan your items.", "example_vi": "Thu ngân sẽ quét các mặt hàng của bạn."},
            {"word": "customer", "meaning": "khách hàng", "phonetic": "/ˈkʌs.tə.mɚ/", "example": "We value our loyal customers.", "example_vi": "Chúng tôi trân trọng những khách hàng trung thành."},
            {"word": "boutique", "meaning": "cửa hàng thời trang nhỏ", "phonetic": "/buːˈtiːk/", "example": "She bought a dress at a local boutique.", "example_vi": "Cô ấy đã mua một chiếc váy tại một cửa hàng thời trang nhỏ."},
            {"word": "apparel", "meaning": "quần áo, trang phục", "phonetic": "/əˈper.əl/", "example": "They sell men's and women's apparel.", "example_vi": "Họ bán trang phục cho cả nam và nữ."},
            {"word": "wardrobe", "meaning": "tủ quần áo", "phonetic": "/ˈwɔːr.droʊb/", "example": "I need to update my summer wardrobe.", "example_vi": "Tôi cần cập nhật tủ quần áo mùa hè."},
            {"word": "trendy", "meaning": "hợp thời trang", "phonetic": "/ˈtren.di/", "example": "She always wears trendy clothes.", "example_vi": "Cô ấy luôn mặc quần áo hợp thời."},
            {"word": "vintage", "meaning": "cổ điển", "phonetic": "/ˈvɪn.t̬ɪdʒ/", "example": "He collects vintage watches.", "example_vi": "Anh ấy sưu tầm đồng hồ cổ điển."},
            {"word": "brand", "meaning": "thương hiệu", "phonetic": "/brænd/", "example": "What is your favorite clothing brand?", "example_vi": "Thương hiệu quần áo yêu thích của bạn là gì?"},
            {"word": "fabric", "meaning": "vải", "phonetic": "/ˈfæb.rɪk/", "example": "Cotton is a comfortable fabric.", "example_vi": "Cotton là loại vải thoải mái."},
            {"word": "outfit", "meaning": "bộ trang phục", "phonetic": "/ˈaʊt.fɪt/", "example": "She wore a stunning outfit to the party.", "example_vi": "Cô ấy mặc một bộ trang phục tuyệt đẹp đến bữa tiệc."},
            {"word": "accessory", "meaning": "phụ kiện", "phonetic": "/əkˈses.ɚ.i/", "example": "Belts and hats are fashion accessories.", "example_vi": "Thắt lưng và mũ là những phụ kiện thời trang."},
            {"word": "mall", "meaning": "trung tâm mua sắm", "phonetic": "/mɑːl/", "example": "We spent the whole day at the shopping mall.", "example_vi": "Chúng tôi dành cả ngày tại trung tâm mua sắm."},
            {"word": "grocery", "meaning": "cửa hàng tạp hóa", "phonetic": "/ˈɡroʊ.sɚ.i/", "example": "I need to buy some groceries for dinner.", "example_vi": "Tôi cần mua đồ tạp hóa cho bữa tối."},
            {"word": "supermarket", "meaning": "siêu thị", "phonetic": "/ˈsuː.pɚˌmɑːr.kɪt/", "example": "The supermarket is open until 10 PM.", "example_vi": "Siêu thị mở cửa đến 10 giờ tối."},
            {"word": "aisle", "meaning": "lối đi (giữa các kệ hàng)", "phonetic": "/aɪl/", "example": "You can find milk in the dairy aisle.", "example_vi": "Bạn có thể tìm sữa ở lối đi sản phẩm bơ sữa."},
            {"word": "trolley", "meaning": "xe đẩy hàng", "phonetic": "/ˈtrɑː.li/", "example": "Push the trolley to the checkout.", "example_vi": "Đẩy xe hàng đến quầy thanh toán."},
            {"word": "basket", "meaning": "giỏ hàng", "phonetic": "/ˈbæs.kət/", "example": "I only need a basket, not a trolley.", "example_vi": "Tôi chỉ cần một giỏ hàng, không cần xe đẩy."},
            {"word": "checkout", "meaning": "quầy thanh toán", "phonetic": "/ˈtʃek.aʊt/", "example": "There is a long line at the checkout.", "example_vi": "Có hàng dài ở quầy thanh toán."},
            {"word": "wallet", "meaning": "ví tiền", "phonetic": "/ˈwɑː.lɪt/", "example": "I lost my wallet yesterday.", "example_vi": "Tôi đã mất ví vào hôm qua."},
            {"word": "credit card", "meaning": "thẻ tín dụng", "phonetic": "/ˈkred.ɪt kɑːrd/", "example": "Do you accept credit cards?", "example_vi": "Bạn có nhận thẻ tín dụng không?"},
            {"word": "cash", "meaning": "tiền mặt", "phonetic": "/kæʃ/", "example": "I prefer to pay in cash.", "example_vi": "Tôi thích trả bằng tiền mặt."},
            {"word": "expensive", "meaning": "đắt đỏ", "phonetic": "/ɪkˈspen.sɪv/", "example": "That designer bag is too expensive.", "example_vi": "Chiếc túi hiệu đó quá đắt."},
            {"word": "cheap", "meaning": "rẻ", "phonetic": "/tʃiːp/", "example": "I bought some cheap clothes at the market.", "example_vi": "Tôi đã mua một số quần áo rẻ ở chợ."},
            {"word": "try on", "meaning": "thử (quần áo)", "phonetic": "/traɪ ɑːn/", "example": "Can I try this shirt on?", "example_vi": "Tôi có thể thử chiếc áo này không?"},
            {"word": "fit", "meaning": "vừa vặn", "phonetic": "/fɪt/", "example": "These shoes don't fit me.", "example_vi": "Đôi giày này không vừa với tôi."},
            {"word": "size", "meaning": "kích cỡ", "phonetic": "/saɪz/", "example": "What size do you wear?", "example_vi": "Bạn mặc cỡ nào?"}
        ]
    },
    {
        "id": "housing",
        "name": "Housing & Furniture",
        "icon": "🏠",
        "words": [
            {"word": "apartment", "meaning": "căn hộ", "phonetic": "/əˈpɑːrt.mənt/", "example": "They live in a modern apartment in the city.", "example_vi": "Họ sống trong một căn hộ hiện đại trong thành phố."},
            {"word": "balcony", "meaning": "ban công", "phonetic": "/ˈbæl.kə.ni/", "example": "We drank coffee on the balcony.", "example_vi": "Chúng tôi uống cà phê trên ban công."},
            {"word": "basement", "meaning": "tầng hầm", "phonetic": "/ˈbeɪs.mənt/", "example": "The washing machine is in the basement.", "example_vi": "Máy giặt ở tầng hầm."},
            {"word": "ceiling", "meaning": "trần nhà", "phonetic": "/ˈsiː.lɪŋ/", "example": "The room has a very high ceiling.", "example_vi": "Căn phòng có trần nhà rất cao."},
            {"word": "chimney", "meaning": "ống khói", "phonetic": "/ˈtʃɪm.ni/", "example": "Smoke was coming out of the chimney.", "example_vi": "Khói đang bay ra từ ống khói."},
            {"word": "corridor", "meaning": "hành lang", "phonetic": "/ˈkɔːr.ə.dɚ/", "example": "His office is at the end of the corridor.", "example_vi": "Văn phòng của anh ấy ở cuối hành lang."},
            {"word": "furniture", "meaning": "đồ nội thất", "phonetic": "/ˈfɝː.nɪ.tʃɚ/", "example": "They bought new furniture for the living room.", "example_vi": "Họ mua nội thất mới cho phòng khách."},
            {"word": "carpet", "meaning": "tấm thảm", "phonetic": "/ˈkɑːr.pət/", "example": "He spilled wine on the carpet.", "example_vi": "Anh ta đổ rượu lên tấm thảm."},
            {"word": "curtain", "meaning": "rèm cửa", "phonetic": "/ˈkɝː.t̬ən/", "example": "Please close the curtains.", "example_vi": "Vui lòng kéo rèm lại."},
            {"word": "cushion", "meaning": "gối tựa", "phonetic": "/ˈkʊʃ.ən/", "example": "She placed a cushion on the sofa.", "example_vi": "Cô ấy đặt một chiếc gối tựa lên ghế sofa."},
            {"word": "mattress", "meaning": "nệm", "phonetic": "/ˈmæt.rəs/", "example": "This mattress is very comfortable.", "example_vi": "Tấm nệm này rất thoải mái."},
            {"word": "wardrobe", "meaning": "tủ quần áo", "phonetic": "/ˈwɔːr.droʊb/", "example": "Hang your coat in the wardrobe.", "example_vi": "Treo áo khoác của bạn vào tủ quần áo."},
            {"word": "drawer", "meaning": "ngăn kéo", "phonetic": "/drɔːr/", "example": "The keys are in the top drawer.", "example_vi": "Chìa khóa ở trong ngăn kéo trên cùng."},
            {"word": "bookshelf", "meaning": "giá sách", "phonetic": "/ˈbʊk.ʃelf/", "example": "Put the book back on the bookshelf.", "example_vi": "Đặt sách lại lên giá sách."},
            {"word": "mirror", "meaning": "cái gương", "phonetic": "/ˈmɪr.ɚ/", "example": "She looked at herself in the mirror.", "example_vi": "Cô ấy nhìn mình trong gương."},
            {"word": "tenant", "meaning": "người thuê nhà", "phonetic": "/ˈten.ənt/", "example": "The landlord is looking for a new tenant.", "example_vi": "Chủ nhà đang tìm người thuê mới."},
            {"word": "landlord", "meaning": "chủ nhà", "phonetic": "/ˈlænd.lɔːrd/", "example": "My landlord is very friendly.", "example_vi": "Chủ nhà của tôi rất thân thiện."},
            {"word": "mortgage", "meaning": "thế chấp", "phonetic": "/ˈmɔːr.ɡɪdʒ/", "example": "They took out a mortgage to buy the house.", "example_vi": "Họ đã vay thế chấp để mua ngôi nhà."},
            {"word": "rent", "meaning": "tiền thuê nhà", "phonetic": "/rent/", "example": "The rent is due on the first of the month.", "example_vi": "Tiền thuê đến hạn vào ngày đầu tháng."},
            {"word": "deposit", "meaning": "tiền đặt cọc", "phonetic": "/dɪˈpɑː.zɪt/", "example": "You need to pay a deposit before moving in.", "example_vi": "Bạn cần đặt cọc trước khi dọn vào."},
            {"word": "neighborhood", "meaning": "khu vực lân cận", "phonetic": "/ˈneɪ.bɚ.hʊd/", "example": "This is a quiet and safe neighborhood.", "example_vi": "Đây là một khu phố yên tĩnh và an toàn."},
            {"word": "suburb", "meaning": "vùng ngoại ô", "phonetic": "/ˈsʌb.ɝːb/", "example": "Many families prefer to live in the suburbs.", "example_vi": "Nhiều gia đình thích sống ở vùng ngoại ô."},
            {"word": "mansion", "meaning": "dinh thự", "phonetic": "/ˈmæn.ʃən/", "example": "He lives in a huge mansion.", "example_vi": "Anh ấy sống trong một dinh thự lớn."},
            {"word": "garage", "meaning": "nhà để xe", "phonetic": "/ɡəˈrɑːʒ/", "example": "Park the car in the garage.", "example_vi": "Đậu xe trong nhà để xe."},
            {"word": "fence", "meaning": "hàng rào", "phonetic": "/fens/", "example": "The dog jumped over the wooden fence.", "example_vi": "Con chó đã nhảy qua hàng rào gỗ."},
            {"word": "lawn", "meaning": "bãi cỏ", "phonetic": "/lɑːn/", "example": "He is mowing the lawn right now.", "example_vi": "Anh ấy đang cắt cỏ ngay lúc này."},
            {"word": "porch", "meaning": "hiên nhà", "phonetic": "/pɔːrtʃ/", "example": "We sat on the porch and watched the rain.", "example_vi": "Chúng tôi ngồi trên hiên và ngắm mưa."},
            {"word": "attic", "meaning": "gác xép", "phonetic": "/ˈæt̬.ɪk/", "example": "They store old clothes in the attic.", "example_vi": "Họ cất quần áo cũ trong gác xép."},
            {"word": "appliance", "meaning": "thiết bị gia dụng", "phonetic": "/əˈplaɪ.əns/", "example": "We sell kitchen appliances like ovens and fridges.", "example_vi": "Chúng tôi bán thiết bị gia dụng như lò nướng và tủ lạnh."},
            {"word": "renovate", "meaning": "cải tạo", "phonetic": "/ˈren.ə.veɪt/", "example": "They plan to renovate the old house.", "example_vi": "Họ dự định cải tạo ngôi nhà cũ."}
        ]
    },
    {
        "id": "weather",
        "name": "Weather & Environment",
        "icon": "🌤️",
        "words": [
            {"word": "climate", "meaning": "khí hậu", "phonetic": "/ˈklaɪ.mət/", "example": "The climate here is very tropical.", "example_vi": "Khí hậu ở đây rất nhiệt đới."},
            {"word": "temperature", "meaning": "nhiệt độ", "phonetic": "/ˈtem.pɚ.ə.tʃɚ/", "example": "The temperature dropped to freezing.", "example_vi": "Nhiệt độ giảm xuống mức đóng băng."},
            {"word": "forecast", "meaning": "dự báo", "phonetic": "/ˈfɔːr.kæst/", "example": "The weather forecast says it will rain tomorrow.", "example_vi": "Dự báo thời tiết nói ngày mai sẽ mưa."},
            {"word": "hurricane", "meaning": "bão lớn", "phonetic": "/ˈhɝː.ɪ.kən/", "example": "A powerful hurricane hit the coast.", "example_vi": "Một cơn bão lớn đã đổ bộ vào bờ biển."},
            {"word": "tornado", "meaning": "lốc xoáy", "phonetic": "/tɔːrˈneɪ.doʊ/", "example": "The tornado destroyed several houses.", "example_vi": "Cơn lốc xoáy đã phá hủy nhiều ngôi nhà."},
            {"word": "blizzard", "meaning": "bão tuyết", "phonetic": "/ˈblɪz.ɚd/", "example": "We were stuck at home during the blizzard.", "example_vi": "Chúng tôi mắc kẹt ở nhà trong suốt cơn bão tuyết."},
            {"word": "drought", "meaning": "hạn hán", "phonetic": "/draʊt/", "example": "The severe drought ruined the crops.", "example_vi": "Đợt hạn hán nghiêm trọng đã phá hoại mùa màng."},
            {"word": "flood", "meaning": "lũ lụt", "phonetic": "/flʌd/", "example": "Heavy rain caused a flood in the city.", "example_vi": "Mưa lớn gây lũ lụt trong thành phố."},
            {"word": "breeze", "meaning": "gió nhẹ", "phonetic": "/briːz/", "example": "A cool breeze blew through the window.", "example_vi": "Một làn gió nhẹ thổi qua cửa sổ."},
            {"word": "humid", "meaning": "ẩm ướt", "phonetic": "/ˈhjuː.mɪd/", "example": "The weather is hot and humid today.", "example_vi": "Thời tiết hôm nay nóng và ẩm ướt."},
            {"word": "foggy", "meaning": "có sương mù", "phonetic": "/ˈfɑː.ɡi/", "example": "It's too foggy to drive safely.", "example_vi": "Sương mù quá dày để lái xe an toàn."},
            {"word": "pollution", "meaning": "sự ô nhiễm", "phonetic": "/pəˈluː.ʃən/", "example": "Air pollution is a major problem in big cities.", "example_vi": "Ô nhiễm không khí là vấn đề lớn ở các thành phố lớn."},
            {"word": "ecosystem", "meaning": "hệ sinh thái", "phonetic": "/ˈiː.koʊˌsɪs.təm/", "example": "Plastic waste is destroying the marine ecosystem.", "example_vi": "Rác thải nhựa đang phá hủy hệ sinh thái biển."},
            {"word": "habitat", "meaning": "môi trường sống", "phonetic": "/ˈhæb.ə.tæt/", "example": "The panda's natural habitat is disappearing.", "example_vi": "Môi trường sống tự nhiên của gấu trúc đang dần biến mất."},
            {"word": "conservation", "meaning": "sự bảo tồn", "phonetic": "/ˌkɑːn.sɚˈveɪ.ʃən/", "example": "Wildlife conservation is essential.", "example_vi": "Bảo tồn động vật hoang dã là điều cần thiết."},
            {"word": "renewable", "meaning": "có thể tái tạo", "phonetic": "/rɪˈnuː.ə.bəl/", "example": "We should use renewable energy like solar power.", "example_vi": "Chúng ta nên sử dụng năng lượng tái tạo như năng lượng mặt trời."},
            {"word": "sustainable", "meaning": "bền vững", "phonetic": "/səˈsteɪ.nə.bəl/", "example": "Sustainable farming protects the environment.", "example_vi": "Nông nghiệp bền vững bảo vệ môi trường."},
            {"word": "recycle", "meaning": "tái chế", "phonetic": "/ˌriːˈsaɪ.kəl/", "example": "Always recycle glass and plastic bottles.", "example_vi": "Luôn tái chế chai thủy tinh và nhựa."},
            {"word": "biodegradable", "meaning": "phân hủy sinh học", "phonetic": "/ˌbaɪ.oʊ.dɪˈɡreɪ.də.bəl/", "example": "These bags are 100% biodegradable.", "example_vi": "Những túi này có thể phân hủy sinh học 100%."},
            {"word": "emission", "meaning": "khí thải", "phonetic": "/ɪˈmɪʃ.ən/", "example": "The government aims to cut carbon emissions.", "example_vi": "Chính phủ đặt mục tiêu cắt giảm khí thải carbon."},
            {"word": "greenhouse", "meaning": "nhà kính", "phonetic": "/ˈɡriːn.haʊs/", "example": "The greenhouse effect causes global warming.", "example_vi": "Hiệu ứng nhà kính gây ra sự nóng lên toàn cầu."},
            {"word": "glacier", "meaning": "sông băng", "phonetic": "/ˈɡleɪ.ʃɚ/", "example": "The glaciers are melting at an alarming rate.", "example_vi": "Các sông băng đang tan chảy với tốc độ đáng báo động."},
            {"word": "avalanche", "meaning": "tuyết lở", "phonetic": "/ˈæv.əl.æntʃ/", "example": "Two skiers were caught in an avalanche.", "example_vi": "Hai người trượt tuyết bị kẹt trong trận tuyết lở."},
            {"word": "earthquake", "meaning": "động đất", "phonetic": "/ˈɝːθ.kweɪk/", "example": "Japan experiences many earthquakes.", "example_vi": "Nhật Bản thường xuyên xảy ra động đất."},
            {"word": "volcano", "meaning": "núi lửa", "phonetic": "/vɑːlˈkeɪ.noʊ/", "example": "The active volcano erupted yesterday.", "example_vi": "Ngọn núi lửa đang hoạt động đã phun trào hôm qua."},
            {"word": "atmosphere", "meaning": "khí quyển", "phonetic": "/ˈæt.məs.fɪr/", "example": "The atmosphere protects us from the sun.", "example_vi": "Khí quyển bảo vệ chúng ta khỏi ánh nắng mặt trời."},
            {"word": "ozone", "meaning": "ô-zôn", "phonetic": "/ˈoʊ.zoʊn/", "example": "The ozone layer is recovering.", "example_vi": "Tầng ozone đang dần phục hồi."},
            {"word": "wildlife", "meaning": "động vật hoang dã", "phonetic": "/ˈwaɪld.laɪf/", "example": "The park is famous for its diverse wildlife.", "example_vi": "Công viên nổi tiếng với hệ động vật hoang dã đa dạng."},
            {"word": "extinct", "meaning": "tuyệt chủng", "phonetic": "/ɪkˈstɪŋkt/", "example": "Dinosaurs have been extinct for millions of years.", "example_vi": "Khủng long đã tuyệt chủng hàng triệu năm trước."},
            {"word": "species", "meaning": "loài", "phonetic": "/ˈspiː.ʃiːz/", "example": "Many plant species are in danger.", "example_vi": "Nhiều loài thực vật đang trong tình trạng nguy hiểm."}
        ]
    },
    {
        "id": "entertainment",
        "name": "Entertainment & Media",
        "icon": "🎬",
        "words": [
            {"word": "audience", "meaning": "khán giả", "phonetic": "/ˈɑː.di.əns/", "example": "The audience clapped loudly after the show.", "example_vi": "Khán giả vỗ tay nhiệt liệt sau buổi biểu diễn."},
            {"word": "broadcast", "meaning": "phát sóng", "phonetic": "/ˈbrɑːd.kæst/", "example": "The interview will be broadcast live.", "example_vi": "Cuộc phỏng vấn sẽ được phát sóng trực tiếp."},
            {"word": "celebrity", "meaning": "người nổi tiếng", "phonetic": "/səˈleb.rə.t̬i/", "example": "Many celebrities attended the gala.", "example_vi": "Nhiều người nổi tiếng đã tham dự buổi dạ tiệc."},
            {"word": "channel", "meaning": "kênh", "phonetic": "/ˈtʃæn.əl/", "example": "What channel is the football match on?", "example_vi": "Trận bóng đá phát trên kênh nào vậy?"},
            {"word": "commercial", "meaning": "quảng cáo", "phonetic": "/kəˈmɝː.ʃəl/", "example": "I hate watching TV commercials.", "example_vi": "Tôi ghét xem quảng cáo trên TV."},
            {"word": "documentary", "meaning": "phim tài liệu", "phonetic": "/ˌdɑː.kjəˈmen.t̬ɚ.i/", "example": "I watched a documentary about polar bears.", "example_vi": "Tôi đã xem một bộ phim tài liệu về gấu Bắc Cực."},
            {"word": "episode", "meaning": "tập phim", "phonetic": "/ˈep.ə.soʊd/", "example": "Have you seen the latest episode?", "example_vi": "Bạn đã xem tập mới nhất chưa?"},
            {"word": "genre", "meaning": "thể loại", "phonetic": "/ˈʒɑ̃ː.rə/", "example": "What is your favorite music genre?", "example_vi": "Thể loại nhạc yêu thích của bạn là gì?"},
            {"word": "journalism", "meaning": "nghề báo", "phonetic": "/ˈdʒɝː.nə.lɪ.zəm/", "example": "He has a degree in journalism.", "example_vi": "Anh ấy có bằng đại học về báo chí."},
            {"word": "magazine", "meaning": "tạp chí", "phonetic": "/ˈmæɡ.ə.ziːn/", "example": "She reads fashion magazines every month.", "example_vi": "Cô ấy đọc tạp chí thời trang mỗi tháng."},
            {"word": "media", "meaning": "truyền thông", "phonetic": "/ˈmiː.di.ə/", "example": "The mass media has a strong influence on people.", "example_vi": "Phương tiện truyền thông đại chúng có ảnh hưởng mạnh đến con người."},
            {"word": "orchestra", "meaning": "dàn nhạc", "phonetic": "/ˈɔːr.kə.strə/", "example": "The orchestra played a beautiful symphony.", "example_vi": "Dàn nhạc đã chơi một bản giao hưởng tuyệt đẹp."},
            {"word": "performance", "meaning": "buổi biểu diễn", "phonetic": "/pɚˈfɔːr.məns/", "example": "Her performance was outstanding.", "example_vi": "Màn biểu diễn của cô ấy thật xuất sắc."},
            {"word": "podcast", "meaning": "tệp phát thanh", "phonetic": "/ˈpɑːd.kæst/", "example": "I listen to podcasts while driving.", "example_vi": "Tôi nghe podcast khi lái xe."},
            {"word": "producer", "meaning": "nhà sản xuất", "phonetic": "/prəˈduː.sɚ/", "example": "He is a famous Hollywood movie producer.", "example_vi": "Anh ấy là một nhà sản xuất phim Hollywood nổi tiếng."},
            {"word": "publication", "meaning": "sự xuất bản", "phonetic": "/ˌpʌb.ləˈkeɪ.ʃən/", "example": "The book is ready for publication.", "example_vi": "Cuốn sách đã sẵn sàng để xuất bản."},
            {"word": "review", "meaning": "bài đánh giá", "phonetic": "/rɪˈvjuː/", "example": "The movie received positive reviews.", "example_vi": "Bộ phim nhận được nhiều đánh giá tích cực."},
            {"word": "script", "meaning": "kịch bản", "phonetic": "/skrɪpt/", "example": "The actors are memorizing the script.", "example_vi": "Các diễn viên đang học thuộc kịch bản."},
            {"word": "sponsor", "meaning": "nhà tài trợ", "phonetic": "/ˈspɑːn.sɚ/", "example": "Nike is a major sponsor of the event.", "example_vi": "Nike là nhà tài trợ chính của sự kiện."},
            {"word": "stream", "meaning": "phát trực tuyến", "phonetic": "/striːm/", "example": "You can stream the movie online.", "example_vi": "Bạn có thể xem phim trực tuyến."},
            {"word": "studio", "meaning": "phòng thu", "phonetic": "/ˈstuː.di.oʊ/", "example": "They are recording a new song in the studio.", "example_vi": "Họ đang thu âm một bài hát mới trong phòng thu."},
            {"word": "subtitle", "meaning": "phụ đề", "phonetic": "/ˈsʌbˌtaɪ.t̬əl/", "example": "I prefer watching foreign movies with subtitles.", "example_vi": "Tôi thích xem phim nước ngoài có phụ đề."},
            {"word": "talent", "meaning": "tài năng", "phonetic": "/ˈtæl.ənt/", "example": "She has a natural talent for singing.", "example_vi": "Cô ấy có tài năng thiên bẩm về ca hát."},
            {"word": "theater", "meaning": "nhà hát", "phonetic": "/ˈθiː.ə.t̬ɚ/", "example": "We went to the theater to see a play.", "example_vi": "Chúng tôi đến nhà hát để xem một vở kịch."},
            {"word": "ticket", "meaning": "vé", "phonetic": "/ˈtɪk.ɪt/", "example": "I bought two tickets for the concert.", "example_vi": "Tôi đã mua hai vé cho buổi hòa nhạc."},
            {"word": "viewer", "meaning": "người xem", "phonetic": "/ˈvjuː.ɚ/", "example": "The show has millions of viewers worldwide.", "example_vi": "Chương trình có hàng triệu người xem trên toàn thế giới."},
            {"word": "viral", "meaning": "lan truyền", "phonetic": "/ˈvaɪ.rəl/", "example": "The video went viral on social media.", "example_vi": "Video đó đã lan truyền chóng mặt trên mạng xã hội."},
            {"word": "volume", "meaning": "âm lượng", "phonetic": "/ˈvɑːl.juːm/", "example": "Please turn down the volume.", "example_vi": "Vui lòng vặn nhỏ âm lượng xuống."},
            {"word": "album", "meaning": "album nhạc", "phonetic": "/ˈæl.bəm/", "example": "Their new album is fantastic.", "example_vi": "Album mới của họ thật tuyệt vời."},
            {"word": "cinema", "meaning": "rạp chiếu phim", "phonetic": "/ˈsɪn.ə.mə/", "example": "Let's go to the cinema tonight.", "example_vi": "Tối nay hãy đi xem phim nhé."}
        ]
    },
    {
        "id": "emotions",
        "name": "Emotions & Personality",
        "icon": "❤️",
        "words": [
            {"word": "affection", "meaning": "tình cảm", "phonetic": "/əˈfek.ʃən/", "example": "She felt great affection for her grandparents.", "example_vi": "Cô ấy cảm thấy tình cảm sâu sắc với ông bà."},
            {"word": "anxiety", "meaning": "sự lo âu", "phonetic": "/æŋˈzaɪ.ə.t̬i/", "example": "He suffers from social anxiety.", "example_vi": "Anh ấy bị chứng lo âu xã hội."},
            {"word": "arrogant", "meaning": "kiêu ngạo", "phonetic": "/ˈær.ə.ɡənt/", "example": "He is too arrogant to ask for help.", "example_vi": "Anh ấy quá kiêu ngạo để nhờ giúp đỡ."},
            {"word": "compassion", "meaning": "lòng thương trắc ẩn", "phonetic": "/kəmˈpæʃ.ən/", "example": "She showed compassion for the homeless man.", "example_vi": "Cô ấy thể hiện lòng trắc ẩn với người vô gia cư."},
            {"word": "confident", "meaning": "tự tin", "phonetic": "/ˈkɑːn.fə.dənt/", "example": "I am confident that we will win.", "example_vi": "Tôi tự tin rằng chúng ta sẽ thắng."},
            {"word": "curious", "meaning": "tò mò", "phonetic": "/ˈkjʊr.i.əs/", "example": "Children are naturally curious about the world.", "example_vi": "Trẻ em tự nhiên hay tò mò về thế giới."},
            {"word": "depressed", "meaning": "trầm cảm", "phonetic": "/dɪˈprest/", "example": "He felt very depressed after losing his job.", "example_vi": "Anh ấy cảm thấy rất trầm cảm sau khi mất việc."},
            {"word": "empathy", "meaning": "sự đồng cảm", "phonetic": "/ˈem.pə.θi/", "example": "Nurses need to have empathy for their patients.", "example_vi": "Y tá cần có sự đồng cảm với bệnh nhân."},
            {"word": "enthusiastic", "meaning": "nhiệt tình", "phonetic": "/ɪnˌθuː.ziˈæs.tɪk/", "example": "She was very enthusiastic about the new project.", "example_vi": "Cô ấy rất nhiệt tình với dự án mới."},
            {"word": "frustrated", "meaning": "tuyệt vọng, nản lòng", "phonetic": "/ˈfrʌs.treɪ.t̬ɪd/", "example": "I feel frustrated when things go wrong.", "example_vi": "Tôi cảm thấy nản lòng khi mọi thứ đi không đúng hướng."},
            {"word": "generous", "meaning": "hào phóng", "phonetic": "/ˈdʒen.ɚ.əs/", "example": "It was very generous of you to pay for dinner.", "example_vi": "Bạn thật hào phóng khi trả tiền cho bữa tối."},
            {"word": "grateful", "meaning": "biết ơn", "phonetic": "/ˈɡreɪt.fəl/", "example": "I am grateful for all your help.", "example_vi": "Tôi biết ơn vì sự giúp đỡ của bạn."},
            {"word": "greedy", "meaning": "tham lam", "phonetic": "/ˈɡriː.di/", "example": "He is a greedy and selfish person.", "example_vi": "Anh ta là một người tham lam và ích kỷ."},
            {"word": "guilty", "meaning": "tội lỗi", "phonetic": "/ˈɡɪl.ti/", "example": "She felt guilty about lying to her mother.", "example_vi": "Cô ấy cảm thấy tội lỗi khi nói dối mẹ."},
            {"word": "honest", "meaning": "trung thực", "phonetic": "/ˈɑː.nɪst/", "example": "To be honest, I didn't like the food.", "example_vi": "Thật ra mà nói, tôi không thích món ăn đó."},
            {"word": "impatient", "meaning": "thiếu kiên nhẫn", "phonetic": "/ɪmˈpeɪ.ʃənt/", "example": "Don't be so impatient!", "example_vi": "Đừng thiếu kiên nhẫn như vậy!"},
            {"word": "jealous", "meaning": "ghen tị", "phonetic": "/ˈdʒel.əs/", "example": "He was jealous of his brother's success.", "example_vi": "Anh ta ghen tị với thành công của anh trai."},
            {"word": "lonely", "meaning": "cô đơn", "phonetic": "/ˈloʊn.li/", "example": "She felt very lonely in the new city.", "example_vi": "Cô ấy cảm thấy rất cô đơn ở thành phố mới."},
            {"word": "modest", "meaning": "khiêm tốn", "phonetic": "/ˈmɑː.dɪst/", "example": "He is very modest about his achievements.", "example_vi": "Anh ấy rất khiêm tốn về những thành tích của mình."},
            {"word": "nervous", "meaning": "lo lắng", "phonetic": "/ˈnɝː.vəs/", "example": "I always get nervous before exams.", "example_vi": "Tôi luôn lo lắng trước các kỳ thi."},
            {"word": "optimistic", "meaning": "lạc quan", "phonetic": "/ˌɑːp.təˈmɪs.tɪk/", "example": "She is optimistic about the future.", "example_vi": "Cô ấy lạc quan về tương lai."},
            {"word": "pessimistic", "meaning": "bi quan", "phonetic": "/ˌpes.əˈmɪs.tɪk/", "example": "Don't be so pessimistic!", "example_vi": "Đừng bi quan như vậy!"},
            {"word": "polite", "meaning": "lịch sự", "phonetic": "/pəˈlaɪt/", "example": "The children were very polite.", "example_vi": "Bọn trẻ rất lịch sự."},
            {"word": "proud", "meaning": "tự hào", "phonetic": "/praʊd/", "example": "His parents are very proud of him.", "example_vi": "Bố mẹ anh ấy rất tự hào về anh ấy."},
            {"word": "relieved", "meaning": "nhẹ nhõm", "phonetic": "/rɪˈliːvd/", "example": "I was relieved to hear you arrived safely.", "example_vi": "Tôi thấy nhẹ nhõm khi nghe bạn đến nơi an toàn."},
            {"word": "rude", "meaning": "thô lỗ", "phonetic": "/ruːd/", "example": "It is rude to interrupt people.", "example_vi": "Ngắt lời người khác là thô lỗ."},
            {"word": "selfish", "meaning": "ích kỷ", "phonetic": "/ˈsel.fɪʃ/", "example": "It's selfish to keep all the candy for yourself.", "example_vi": "Giữ hết kẹo cho mình là ích kỷ."},
            {"word": "shy", "meaning": "nhút nhát", "phonetic": "/ʃaɪ/", "example": "He was too shy to speak to her.", "example_vi": "Anh ấy quá nhút nhát để nói chuyện với cô ấy."},
            {"word": "stubborn", "meaning": "bướng bỉnh", "phonetic": "/ˈstʌb.ɚn/", "example": "She is as stubborn as a mule.", "example_vi": "Cô ấy bướng bỉnh như con la."},
            {"word": "sympathy", "meaning": "sự cảm thông", "phonetic": "/ˈsɪm.pə.θi/", "example": "We express our deepest sympathy to the family.", "example_vi": "Chúng tôi xin gửi lời chia buồn sâu sắc nhất đến gia đình."}
        ]
    }
]

# Add topic_id, image_url (Pollinations AI) to all new topic words
for topic in new_topics_data:
    topic_id = topic["id"]
    for word in topic["words"]:
        word["topic"] = topic["name"]
        # Pollinations supports spaces in prompt, but replacing with %20 is safer.
        # The user's prompt shows writing it normally or joining. Let's just use the raw word url-encoded or replace spaces with %20.
        import urllib.parse
        encoded_word = urllib.parse.quote(word["word"])
        word["image_url"] = f"https://image.pollinations.ai/prompt/{encoded_word}?width=400&height=300&nologo=true"

# Also set image_url for legacy topics (business, travel, daily)
for topic in topics:
    topic_id = topic["id"]
    for word in topic["words"]:
        import urllib.parse
        encoded_word = urllib.parse.quote(word["word"])
        word["image_url"] = f"https://image.pollinations.ai/prompt/{encoded_word}?width=400&height=300&nologo=true"

topics.extend(new_topics_data)

final_data = {
    "topics": topics
}

with open("c:/Project/englishw/data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("data.json generated successfully with example_vi and stable image URLs!")
