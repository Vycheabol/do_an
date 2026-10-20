HỆ THỐNG ẨN DANH HÓA DỮ LIỆU THÔNG MINH

1. Giới thiệu

Đây là đồ án xây dựng một hệ thống ẩn danh hóa dữ liệu.

Mục tiêu chính của hệ thống là cố gắng cân bằng giữa 2 vấn đề:

Bảo vệ quyền riêng tư của dữ liệu

Giữ lại độ hữu ích của dữ liệu để còn có thể dùng cho Machine Learning

Trong đồ án có sử dụng một số kỹ thuật như:

Generalization

Suppression

k-anonymity

l-diversity

Đánh giá Utility bằng Machine Learning

Sinh nhiều Strategy

Xếp hạng và chọn Strategy phù hợp

Phần giao diện của hệ thống được làm bằng Streamlit.

2. Luồng hoạt động chính

Hệ thống hoạt động theo luồng như sau:

Dataset

↓

Kiểm tra cấu trúc dữ liệu

↓

Sinh các Candidate Strategy

↓

Generalization + Suppression

↓

Đánh giá k-anonymity và l-diversity

↓

Đánh giá Utility bằng Machine Learning

↓

Tính Data Retention

↓

Tính Selection Score

↓

Xếp hạng Candidate

↓

Chọn Candidate phù hợp nhất

↓

Final Test

↓

Vẽ biểu đồ kết quả

↓

Xuất dataset ẩn danh cuối cùng

3. Cấu trúc project

Do_an_project/
│
├── anon_app/
│   └── app.py
│
├── data/
│
├── notebooks/
│   ├── 01_khao_sat_du_lieu.ipynb
│   └── 02_danh_gia_machine_learning.ipynb
│
├── outputs_bieu_do_ket_qua/
│
├── src/
│   ├── anonymization_engine.py
│   ├── ml_evaluator.py
│   ├── privacy_analyzer.py
│   ├── result_visualizer.py
│   ├── strategy_generator.py
│   ├── strategy_selector.py
│   ├── system_tester.py
│   └── utility_evaluator.py
│
├── pipeline.py
├── requirements.txt
└── README.md

4. Môi trường sử dụng

Đồ án được làm và kiểm thử với:

Python 3.10

pandas 2.3.3

numpy 2.2.6

matplotlib 3.10.9

scikit-learn 1.7.2

streamlit 1.63.0

jupyter 1.1.1

5. Cài đặt môi trường

Bước 1: Tạo virtual environment

python -m venv .venv

Bước 2: Kích hoạt môi trường ảo trên Windows

.venv\Scripts\activate

Bước 3: Cài thư viện

pip install -r requirements.txt

6. Chạy chương trình

Đứng tại thư mục gốc của project rồi chạy:

streamlit run anon_app/app.py

Sau đó giao diện hệ thống sẽ được mở trên trình duyệt.

7. Dataset đầu vào

Trong đồ án hiện tại, hệ thống cần một số cột chính để chạy được pipeline:

tuoi
loai_cong_viec
so_nam_hoc
tinh_trang_hon_nhan
nghe_nghiep
gio_lam_moi_tuan
quoc_gia
thu_nhap

Trong đó:

thu_nhap được dùng làm Sensitive Attribute để kiểm tra l-diversity

thu_nhap cũng được dùng làm Target cho Machine Learning

Hệ thống có thể đọc file CSV dùng dấu phân cách:

dấu phẩy ,

dấu chấm phẩy ;

Nếu dataset bị thiếu các cột bắt buộc thì hệ thống sẽ báo lỗi và không cho chạy tiếp.

Lý do là nếu thiếu các cột này thì các bước Generalization, Privacy hoặc Machine Learning có thể cho kết quả không đúng.

8. Cấu hình Privacy

Người dùng có thể chọn giá trị:

k-anonymity

l-diversity

Trong phần thực nghiệm chính của đồ án đang dùng:

k = 5
l = 2

Hai giá trị này chỉ là ngưỡng được chọn trong phạm vi thực nghiệm của đồ án.

Không được hiểu rằng k=5 và l=2 là yêu cầu bắt buộc của GDPR.

Ngoài ra:

privacy_valid = True

chỉ có nghĩa là Candidate đạt được giá trị k và l mà hệ thống đang yêu cầu.

Nó không có nghĩa là dữ liệu đã chắc chắn đáp ứng toàn bộ GDPR.

9. Utility Score

Trong đồ án, Logistic Regression được dùng để đánh giá ảnh hưởng của ẩn danh hóa tới Machine Learning.

Các metric được tính gồm:

Accuracy

Precision

Recall

F1 Score

Balanced Accuracy

ROC-AUC

Utility Score tổng được tính từ mức độ giữ lại của 4 metric:

Accuracy

F1 Score

Balanced Accuracy

ROC-AUC

Precision và Recall vẫn được hiển thị để theo dõi nhưng không đưa vào Utility Score tổng.

Utility Retention được giới hạn tối đa là 100%.

Lý do là trong đồ án, chỉ số này được hiểu là mức độ giữ lại hiệu năng của dữ liệu sau khi ẩn danh.

Nếu một metric trên dữ liệu ẩn danh tốt hơn dữ liệu gốc thì giá trị đó vẫn chỉ tính tối đa 100% trong Utility Retention.

10. Chọn Strategy

Trước tiên Candidate phải đạt yêu cầu Privacy.

Sau đó hệ thống tính:

Data Retention = 100 - Suppression (%)

Tiếp theo tính:

Selection Score
=
0.5 × Data Retention
+
0.5 × Validation Utility Score

Công thức này là công thức được xây dựng trong phạm vi đồ án để phục vụ việc so sánh các Candidate.

Nó không phải là tiêu chuẩn quốc tế.

Candidate có Selection Score cao nhất trong các Candidate đạt Privacy sẽ được chọn.

Trong đồ án chỉ kết luận Candidate này là phương án tốt nhất trong các Candidate đã được thử.

Không kết luận đây là phương án tối ưu tuyệt đối.

11. Final Test

Candidate được chọn dựa trên kết quả Validation.

Sau khi đã chọn được Candidate thì hệ thống mới dùng tập Test để đánh giá cuối cùng.

Original và Anonymized được kiểm tra trên:

cùng Test indices

cùng Test target

Tập Test không được dùng để chọn Candidate.

Mục đích là tránh việc dùng Test để lựa chọn Strategy rồi lại tiếp tục dùng chính Test đó để đánh giá kết quả cuối.

12. File đầu ra

Sau khi chạy xong, hệ thống cho phép tải một số file:

Dataset ẩn danh

anonymized_<candidate>.csv

Retained indices

retained_indices_<candidate>.csv

Bảng Ranking

candidate_ranking.csv

13. Một số kiểm thử đã làm

Hệ thống đã được chạy với cấu hình chính:

k = 5
l = 2

Ngoài ra có chạy thêm:

k = 6
l = 2

Khi thay đổi giá trị k thì hệ thống có tính lại:

Suppression

Data Retention

Privacy

Utility

Ranking

Final Test

Điều này cho thấy phần cấu hình k và l không bị hard-code cố định ở một giá trị.

Ngoài ra cũng có test dataset thiếu cột bắt buộc.

Ví dụ đổi:

thu_nhap

thành:

thu_nhap_test

thì hệ thống phát hiện thiếu cột thu_nhap và không cho chạy Anonymization.

Hệ thống cũng đã được chỉnh để đọc được file CSV dùng dấu , hoặc ;.

14. Giới hạn của đồ án

Hiện tại hệ thống được xây dựng theo cấu trúc dataset đã dùng trong đồ án.

Nó chưa phải hệ thống có thể tự nhận biết và xử lý mọi dataset bất kỳ.

Nếu dùng dataset có cấu trúc khác thì cần xác định lại:

Quasi-Identifier

Sensitive Attribute

Target

Quy tắc Generalization

Đây cũng là một hướng có thể phát triển thêm sau này.