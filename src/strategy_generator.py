# 1. KHAI BÁO CÁC MỨC GENERALIZATION TUỔI

AVAILABLE_AGE_LEVELS = [
    "age3",
    "age_high"
]

# 2. KHAI BÁO CÁC MỨC GENERALIZATION GIỜ LÀM VIỆC

# Đây là mức tổng quát hóa mạnh hơn.
AVAILABLE_HOURS_LEVELS = [
    "hours3",
    "hours2"
]


# 3. TẠO CẤU HÌNH CHO MỘT CANDIDATE

def create_strategy_config(
    strategy_name,
    age_level,
    hours_level
):
    """
    Tạo cấu hình cho một Candidate Strategy.

    Parameters
    ----------
    strategy_name : str
        Tên Candidate.

    age_level : str
        Mức Generalization tuổi.

    hours_level : str
        Mức Generalization giờ làm việc.

    Returns
    -------
    dict
        Dictionary mô tả Candidate Strategy.
    """


    # 3.1. KIỂM TRA TÊN STRATEGY

    # Tên Strategy phải là chuỗi.
    if not isinstance(
        strategy_name,
        str
    ):

        raise TypeError(
            "strategy_name phải là kiểu chuỗi."
        )


    # Xóa khoảng trắng thừa.
    strategy_name = (
        strategy_name
        .strip()
    )


    # Không cho phép tên rỗng.
    if not strategy_name:

        raise ValueError(
            "strategy_name không được để trống."
        )


    # 3.2. KIỂM TRA AGE LEVEL

    # age_level phải nằm trong danh sách
    # các mức tuổi mà hệ thống hỗ trợ.
    if age_level not in AVAILABLE_AGE_LEVELS:

        raise ValueError(
            "age_level không hợp lệ. "
            f"Các giá trị cho phép: {AVAILABLE_AGE_LEVELS}"
        )

    # 3.3. KIỂM TRA HOURS LEVEL

    # hours_level cũng phải nằm
    # trong danh sách các mức được hỗ trợ.
    if hours_level not in AVAILABLE_HOURS_LEVELS:

        raise ValueError(
            "hours_level không hợp lệ. "
            f"Các giá trị cho phép: {AVAILABLE_HOURS_LEVELS}"
        )


    # 3.4. TẠO CẤU HÌNH CANDIDATE

    # Dictionary này là "bản thiết kế"
    # của Candidate.
    strategy_config = {

        # Tên Candidate.
        "strategy_name":
            strategy_name,

        # Mức Generalization tuổi.
        "age_level":
            age_level,

        # Mức Generalization giờ làm việc.
        "hours_level":
            hours_level
    }


    # Trả cấu hình Candidate.
    return strategy_config


# 4. TỰ ĐỘNG SINH CÁC CANDIDATE STRATEGY

def generate_candidate_strategies():
    """
    Sinh tất cả Candidate từ tổ hợp:

    age_level × hours_level

    Returns
    -------
    list
        Danh sách Candidate Strategy.
    """


    # Danh sách dùng để chứa
    # tất cả Candidate được tạo.
    candidate_strategies = []


    # Biến đếm giúp tự động đặt tên:
    #
    # candidate_1
    # candidate_2
    # candidate_3
    # candidate_4
    candidate_number = 1


    # 4.1. DUYỆT MỨC GENERALIZATION TUỔI

    for age_level in AVAILABLE_AGE_LEVELS:


        # 4.2. DUYỆT MỨC GENERALIZATION GIỜ

        for hours_level in AVAILABLE_HOURS_LEVELS:


            # 4.3. TẠO TÊN CANDIDATE

            strategy_name = (
                f"candidate_{candidate_number}"
            )


            # 4.4. TẠO CẤU HÌNH

            strategy_config = (
                create_strategy_config(

                    # Tên Candidate.
                    strategy_name=strategy_name,

                    # Mức tuổi hiện tại.
                    age_level=age_level,

                    # Mức giờ làm việc hiện tại.
                    hours_level=hours_level
                )
            )


            # 4.5. THÊM VÀO DANH SÁCH

            candidate_strategies.append(
                strategy_config
            )


            # Tăng số thứ tự
            # để Candidate tiếp theo có tên mới.
            candidate_number += 1


    # 4.6. TRẢ DANH SÁCH CANDIDATE

    return candidate_strategies



# 5. TÌM CANDIDATE THEO TÊN

def get_candidate_by_name(
    candidate_strategies,
    strategy_name
):
    """
    Tìm Candidate dựa trên tên.
    """


    # Danh sách Candidate phải là list.
    if not isinstance(
        candidate_strategies,
        list
    ):

        raise TypeError(
            "candidate_strategies phải là list."
        )


    # Duyệt từng Candidate.
    for candidate in candidate_strategies:

        # Nếu đúng tên cần tìm
        # thì trả Candidate đó.
        if (
            candidate[
                "strategy_name"
            ]
            ==
            strategy_name
        ):

            return candidate


    # Nếu không tìm thấy
    # thì báo lỗi.
    raise ValueError(
        f"Không tìm thấy Candidate Strategy: {strategy_name}"
    )


# 6. KIỂM TRA DANH SÁCH CANDIDATE

def validate_candidate_strategies(
    candidate_strategies
):
    """
    Kiểm tra danh sách Candidate
    có hợp lệ hay không.
    """


    # Candidate phải được chứa trong list.
    if not isinstance(
        candidate_strategies,
        list
    ):

        raise TypeError(
            "candidate_strategies phải là list."
        )


    # Không cho phép danh sách rỗng.
    if len(
        candidate_strategies
    ) == 0:

        raise ValueError(
            "Danh sách Candidate đang rỗng."
        )


    # Set dùng để phát hiện
    # Candidate bị trùng tên.
    used_strategy_names = set()


    # Duyệt từng Candidate.
    for candidate in candidate_strategies:


        # Candidate phải là dictionary.
        if not isinstance(
            candidate,
            dict
        ):

            raise TypeError(
                "Mỗi Candidate phải là dictionary."
            )


        # KIỂM TRA CÁC KEY BẮT BUỘC

        required_keys = [
            "strategy_name",
            "age_level",
            "hours_level"
        ]


        # Duyệt từng key bắt buộc.
        for required_key in required_keys:

            # Nếu thiếu key thì dừng.
            if required_key not in candidate:

                raise ValueError(
                    f"Candidate thiếu key '{required_key}'."
                )


        # KIỂM TRA TÊN CANDIDATE
        strategy_name = (
            candidate[
                "strategy_name"
            ]
        )


        # Không được trùng tên.
        if strategy_name in used_strategy_names:

            raise ValueError(
                f"Tên Candidate bị trùng: {strategy_name}"
            )


        # Ghi nhận tên đã sử dụng.
        used_strategy_names.add(
            strategy_name
        )


        # KIỂM TRA AGE LEVEL
        if (
            candidate[
                "age_level"
            ]
            not in AVAILABLE_AGE_LEVELS
        ):

            raise ValueError(
                f"{strategy_name}: age_level không hợp lệ."
            )


        # KIỂM TRA HOURS LEVEL
        if (
            candidate[
                "hours_level"
            ]
            not in AVAILABLE_HOURS_LEVELS
        ):

            raise ValueError(
                f"{strategy_name}: hours_level không hợp lệ."
            )


    # Nếu không có lỗi nào
    # thì toàn bộ Candidate hợp lệ.
    return True


# 7. HIỂN THỊ CANDIDATE
def print_candidate_strategies(
    candidate_strategies
):
    """
    Hiển thị danh sách Candidate trên Console.
    """


    # Hiển thị tổng số Candidate.
    print(
        "Số Candidate:",
        len(
            candidate_strategies
        )
    )


    # Duyệt từng Candidate.
    for candidate in candidate_strategies:


        print(
            "\nStrategy:",
            candidate[
                "strategy_name"
            ]
        )


        # Hiển thị mức tuổi.
        print(
            "Age level:",
            candidate[
                "age_level"
            ]
        )


        # Hiển thị mức giờ làm việc.
        print(
            "Hours level:",
            candidate[
                "hours_level"
            ]
        )


# 8. KIỂM TRA MODULE

# Run strategy_generator.py
# Khi pipeline import module này,
# phần test sẽ không tự chạy.
if __name__ == "__main__":


    # 8.1. SINH CANDIDATE

    candidates = (
        generate_candidate_strategies()
    )


    # 8.2. KIỂM TRA CANDIDATE

    candidates_valid = (
        validate_candidate_strategies(
            candidates
        )
    )


    # 8.3. HIỂN THỊ

    print(
        "===== KIỂM TRA STRATEGY GENERATOR ====="
    )


    print(
        "Danh sách Candidate hợp lệ?:",
        candidates_valid
    )


    print_candidate_strategies(
        candidates
    )


    # 8.4. KIỂM TRA TÌM CANDIDATE

    test_candidate = (
        get_candidate_by_name(

            # Danh sách Candidate.
            candidate_strategies=candidates,

            # Tìm Candidate đầu tiên.
            strategy_name="candidate_1"
        )
    )


    print(
        "\n===== KIỂM TRA TÌM CANDIDATE ====="
    )


    print(
        test_candidate
    )


    print(
        "\nStrategy Generator: Chúc mừng bạn đẫ chạy thành công"
    )