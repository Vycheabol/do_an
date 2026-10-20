# HÀM TÍNH SELECTION SCORE CHO MỘT STRATEGY


def calculate_selection_score(
    suppression_percent,
    utility_score_percent,
    privacy_valid,
    weight_data_retention=0.5,
    weight_utility=0.5
):

    # Tính tỷ lệ dữ liệu còn được giữ lại sau suppression
    # Ví dụ suppression = 6.01%
    # thì data retention = 100 - 6.01 = 93.99%
    data_retention_percent = (
        100
        - suppression_percent
    )


    # Kiểm tra strategy có đạt điều kiện Privacy hay không
    # Privacy là điều kiện bắt buộc trước khi được đem ra xếp hạng
    if not privacy_valid:

        # Nếu Privacy chưa đạt thì strategy không được xem là ứng viên hợp lệ
        # Vì vậy không tính Selection Score cho strategy này
        return {

            # Lưu lại tỷ lệ dữ liệu vẫn được giữ
            "data_retention_%": round(
                data_retention_percent,
                2
            ),

            # Không cho điểm vì strategy không đạt Privacy
            "selection_score": None,

            # False nghĩa là strategy không đủ điều kiện tham gia lựa chọn
            "eligible": False
        }


    # Nếu strategy đã đạt Privacy thì bắt đầu tính Selection Score
    # Điểm gồm hai phần:
    # 50% Data Retention + 50% ML Utility
    selection_score = (

        # Phần điểm dành cho tỷ lệ dữ liệu được giữ lại
        data_retention_percent
        * weight_data_retention

        +

        # Phần điểm dành cho Utility của Machine Learning
        utility_score_percent
        * weight_utility
    )


    # Trả kết quả của strategy về dưới dạng dictionary
    return {

        # Tỷ lệ dữ liệu còn giữ lại sau suppression
        "data_retention_%": round(
            data_retention_percent,
            2
        ),

        # Utility Score mà strategy đạt được
        "utility_score_%": round(
            utility_score_percent,
            2
        ),

        # Selection Score dùng để so sánh với các strategy khác
        "selection_score": round(
            selection_score,
            2
        ),

        # True nghĩa là strategy đã đạt Privacy
        # và đủ điều kiện tham gia xếp hạng
        "eligible": True
    }

# HÀM XẾP HẠNG NHIỀU STRATEGY

# Tạo hàm rank_strategies để:
# 1. Nhận nhiều strategy
# 2. Tính Selection Score cho từng strategy
# 3. Loại các strategy không đạt Privacy
# 4. Xếp hạng strategy từ tốt nhất xuống thấp nhất
def rank_strategies(
    strategies,
    weight_data_retention=0.5,
    weight_utility=0.5
):

    # Tạo danh sách rỗng để lưu kết quả sau khi chấm điểm
    ranking_results = []


    # Lần lượt lấy từng strategy trong danh sách đầu vào
    for strategy in strategies:

        # Gọi hàm calculate_selection_score() đã viết phía trên
        # để tính Data Retention và Selection Score
        score_result = calculate_selection_score(

            # Lấy tỷ lệ suppression của strategy hiện tại
            suppression_percent=strategy["suppression_percent"],

            # Lấy Utility Score trên Validation của strategy hiện tại
            utility_score_percent=strategy["utility_score_percent"],

            # Lấy kết quả Privacy True hoặc False
            privacy_valid=strategy["privacy_valid"],

            # Trọng số dành cho Data Retention
            weight_data_retention=weight_data_retention,

            # Trọng số dành cho ML Utility
            weight_utility=weight_utility
        )


        # Tạo dictionary mới để lưu đầy đủ thông tin của strategy hiện tại
        strategy_result = {

            # Lưu tên strategy để sau này biết kết quả thuộc strategy nào
            "strategy": strategy["strategy"],

            # Lưu tỷ lệ suppression ban đầu
            "suppression_%": strategy["suppression_percent"],

            # Lưu Utility Score trên Validation
            "utility_score_%": strategy["utility_score_percent"],

            # Lưu trạng thái Privacy
            "privacy_valid": strategy["privacy_valid"],

            # Lưu tỷ lệ dữ liệu còn giữ lại do hàm tính ra
            "data_retention_%": score_result["data_retention_%"],

            # Lưu Selection Score
            # Nếu strategy không đạt Privacy thì giá trị này sẽ là None
            "selection_score": score_result["selection_score"],

            # Cho biết strategy có đủ điều kiện tham gia xếp hạng hay không
            "eligible": score_result["eligible"]
        }


        # Thêm kết quả của strategy hiện tại vào danh sách tổng
        ranking_results.append(
            strategy_result
        )


    # Chỉ giữ những strategy đủ điều kiện Privacy
    valid_results = [

        # Lấy từng strategy đã được chấm điểm
        result

        # Duyệt qua toàn bộ kết quả
        for result in ranking_results

        # Chỉ giữ strategy có eligible = True
        if result["eligible"]
    ]


    # Sắp xếp các strategy hợp lệ theo Selection Score
    # reverse=True nghĩa là điểm cao nhất đứng đầu
    valid_results = sorted(
        valid_results,
        key=lambda result: result["selection_score"],
        reverse=True
    )


    # Gắn thứ hạng 1, 2, 3,... cho từng strategy
    for index, result in enumerate(
        valid_results,
        start=1
    ):

        # Thêm trường rank vào kết quả
        result["rank"] = index


    # Trả về danh sách strategy đã được xếp hạng
    return valid_results

# HÀM LỰA CHỌN STRATEGY TỐT NHẤT

# Tạo hàm select_best_strategy để tự động lấy strategy đứng hạng 1
#
# strategies:
#     Danh sách các strategy cần đánh giá
#
# weight_data_retention:
#     Trọng số dành cho tỷ lệ dữ liệu được giữ lại
#     Mặc định là 0.5 tương đương 50%
#
# weight_utility:
#     Trọng số dành cho ML Utility
#     Mặc định là 0.5 tương đương 50%
def select_best_strategy(
    strategies,
    weight_data_retention=0.5,
    weight_utility=0.5
):

    # Gọi hàm rank_strategies() đã viết phía trên
    # Hàm này sẽ chấm điểm và sắp xếp các strategy
    ranking_results = rank_strategies(
        strategies=strategies,
        weight_data_retention=weight_data_retention,
        weight_utility=weight_utility
    )


    # Kiểm tra xem có strategy nào đạt điều kiện Privacy hay không
    # Nếu danh sách rỗng nghĩa là không có strategy hợp lệ
    if len(ranking_results) == 0:

        # Trả về None để báo cho hệ thống biết
        # hiện chưa tìm được strategy nào đủ điều kiện
        return None


    # Vì rank_strategies() đã sắp xếp từ điểm cao xuống thấp
    # phần tử đầu tiên chính là strategy đứng hạng 1
    best_strategy = ranking_results[0]


    # Trả về strategy tốt nhất cho phần main.py sử dụng sau này
    return best_strategy



# HÀM PHÂN TÍCH ĐỘ NHẠY (SENSITIVITY ANALYSIS) CHO TRỌNG SỐ
# Tạo hàm run_weight_sensitivity_analysis để kiểm tra xem
# kết luận "Strategy nào tốt nhất" có bị thay đổi hay không
# khi ta thử nhiều bộ trọng số (weight_data_retention, weight_utility)
# khác nhau, thay vì chỉ dùng đúng 1 bộ 50%/50% cố định.
#
# Đây là bước học thuật quan trọng để trả lời câu hỏi:
# "Tại sao lại chọn trọng số 50/50 mà không phải tỷ lệ khác?"
#
# Nếu Strategy tốt nhất vẫn giữ nguyên qua nhiều bộ trọng số khác nhau,
# ta có cơ sở để nói rằng kết luận của hệ thống là ỔN ĐỊNH (robust),
# không phụ thuộc vào việc chọn trọng số một cách chủ quan.
#
# strategies:
#     Danh sách các strategy cần đánh giá
#     (định dạng giống hệt tham số của rank_strategies)
#
# weight_combinations:
#     Danh sách các cặp (weight_data_retention, weight_utility)
def run_weight_sensitivity_analysis(
    strategies,
    weight_combinations=None
):

    # Nếu người dùng không truyền bộ trọng số cụ thể
    # thì dùng 5 kịch bản mặc định nêu trên
    if weight_combinations is None:

        weight_combinations = [
            (0.3, 0.7),
            (0.4, 0.6),
            (0.5, 0.5),
            (0.6, 0.4),
            (0.7, 0.3)
        ]


    # Danh sách dùng để lưu kết quả của từng kịch bản trọng số
    sensitivity_results = []


    # Duyệt qua từng bộ trọng số cần thử nghiệm
    for weight_data_retention, weight_utility in weight_combinations:

        # Xếp hạng lại toàn bộ strategy với bộ trọng số hiện tại
        ranking_with_this_weight = rank_strategies(
            strategies=strategies,
            weight_data_retention=weight_data_retention,
            weight_utility=weight_utility
        )


        # Duyệt từng strategy đã được xếp hạng
        # để ghi lại vị trí (rank) và điểm số của nó
        # ứng với bộ trọng số đang xét
        for result in ranking_with_this_weight:

            sensitivity_results.append(
                {
                    # Bộ trọng số đang thử nghiệm,
                    # viết dưới dạng dễ đọc, ví dụ "30/70"
                    "weight_data_retention_percent":
                        round(weight_data_retention * 100, 0),

                    "weight_utility_percent":
                        round(weight_utility * 100, 0),

                    # Tên strategy
                    "strategy":
                        result["strategy"],

                    # Selection Score ứng với bộ trọng số này
                    "selection_score":
                        result["selection_score"],

                    # Thứ hạng ứng với bộ trọng số này
                    "rank":
                        result["rank"]
                }
            )


    # Trả về danh sách kết quả của toàn bộ kịch bản trọng số
    # Phần gọi hàm (pipeline.py) sẽ chuyển thành DataFrame để xuất CSV/biểu đồ
    return sensitivity_results


# Tạo hàm is_best_strategy_stable để kiểm tra nhanh xem
# Strategy đứng hạng 1 có giữ nguyên xuyên suốt mọi bộ trọng số hay không.
#
# Đây là kết luận ngắn gọn dùng để in ra màn hình / báo cáo,
# thay vì phải tự đọc từng dòng của bảng sensitivity_results.
def is_best_strategy_stable(
    sensitivity_results
):

    # Lọc ra tất cả các dòng đang đứng hạng 1
    # ứng với từng bộ trọng số khác nhau
    rank_1_rows = [
        row
        for row in sensitivity_results
        if row["rank"] == 1
    ]


    # Lấy ra tập hợp các Strategy khác nhau
    # từng đứng hạng 1 ở ít nhất một bộ trọng số
    strategies_that_won = set(
        row["strategy"]
        for row in rank_1_rows
    )


    # Nếu tập hợp này chỉ có đúng 1 phần tử
    # nghĩa là luôn luôn cùng một Strategy thắng
    # dù đổi trọng số như thế nào
    is_stable = (
        len(strategies_that_won) == 1
    )


    # Trả về:
    # is_stable: True/False
    # winning_strategy: tên Strategy đó (nếu ổn định)
    return {
        "is_stable": is_stable,
        "strategies_that_won": sorted(strategies_that_won)
    }




