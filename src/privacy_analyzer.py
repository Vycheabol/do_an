# HÀM ĐÁNH GIÁ K-ANONYMITY

# Hàm evaluate_privacy() dùng để kiểm tra k-anonymity.
#
# Ý tưởng:
# Các bản ghi có cùng bộ giá trị Quasi-Identifier (QI)
# sẽ được gom thành một equivalence class.
#
# Nếu nhóm nhỏ nhất vẫn có ít nhất k bản ghi
# thì dataset đạt yêu cầu k-anonymity.
def evaluate_privacy(
    dataframe,
    qi_columns,
    k_required=5
):

    # 1. KIỂM TRA ĐẦU VÀO

    # Không thể đánh giá k-anonymity
    # nếu không có cột QI.
    if not qi_columns:

        raise ValueError(
            "Danh sách qi_columns không được để trống."
        )


    # Tìm các cột QI được yêu cầu
    # nhưng không tồn tại trong dataset.
    missing_columns = [
        column
        for column in qi_columns
        if column not in dataframe.columns
    ]


    # Nếu thiếu cột QI thì dừng ngay,
    # tránh tính Privacy sai.
    if missing_columns:

        raise ValueError(
            f"Dataset thiếu các cột QI: {missing_columns}"
        )


    # 2. TẠO EQUIVALENCE CLASS

    # Gom những bản ghi có cùng bộ giá trị QI
    # thành cùng một nhóm.
    #
    # Ví dụ:
    #
    # tuoi_nhom = 30-49
    # nghe_nghiep = Van_phong
    # ...
    #
    # Các bản ghi có cùng bộ QI như trên
    # sẽ nằm trong cùng một equivalence class.
    equivalence_class_sizes = (

        dataframe

        .groupby(

            # Dùng tất cả các cột QI để tạo nhóm
            qi_columns,

            # Giữ cả những nhóm có giá trị thiếu
            dropna=False
        )

        # Đếm số bản ghi trong từng nhóm
        .size()
    )


    # 3. ĐẾM SỐ EQUIVALENCE CLASS

    # Mỗi phần tử trong equivalence_class_sizes
    # tương ứng với một equivalence class.
    so_equivalence_class = len(
        equivalence_class_sizes
    )


    # 4. TÌM GIÁ TRỊ k NHỎ NHẤT
    # Nếu dataset rỗng thì không tồn tại nhóm nào.
    if equivalence_class_sizes.empty:

        # Đặt k_min = 0 để biểu diễn
        # rằng dataset không đạt k-anonymity.
        k_min = 0

    else:

        # Nhóm nhỏ nhất có bao nhiêu bản ghi
        # chính là giá trị k_min.
        k_min = int(
            equivalence_class_sizes.min()
        )


    # 5. TÌM SINGLETON GROUP

    # Singleton là equivalence class
    # chỉ có đúng 1 bản ghi.
    #
    # Đây là trường hợp có nguy cơ nhận diện cao.
    singleton_groups = (
        equivalence_class_sizes[
            equivalence_class_sizes == 1
        ]
    )


    # Đếm số nhóm chỉ có 1 bản ghi.
    so_nhom_1_ban_ghi = len(
        singleton_groups
    )


    # Vì mỗi singleton chỉ có 1 bản ghi
    # nên số bản ghi bị cô lập
    # cũng chính bằng số singleton group.
    so_ban_ghi_bi_co_lap = (
        so_nhom_1_ban_ghi
    )


    # 6. TÍNH TỶ LỆ BẢN GHI BỊ CÔ LẬP

    # Tránh chia cho 0 nếu dataset rỗng.
    if len(dataframe) == 0:

        ty_le_bi_co_lap = 0.0

    else:

        # Công thức:
        #
        # số bản ghi bị cô lập
        # ---------------------- × 100
        # tổng số bản ghi
        ty_le_bi_co_lap = (
            so_ban_ghi_bi_co_lap
            /
            len(dataframe)
            *
            100
        )


    # 7. XÁC ĐỊNH CÁC NHÓM VI PHẠM k

    # Một equivalence class vi phạm k
    # nếu số bản ghi trong nhóm nhỏ hơn k_required.
    #
    # Với k_required = 5:
    #
    # nhóm có 1 bản ghi → vi phạm
    # nhóm có 2 bản ghi → vi phạm
    # nhóm có 3 bản ghi → vi phạm
    # nhóm có 4 bản ghi → vi phạm
    # nhóm có >= 5     → đạt
    violating_groups = (
        equivalence_class_sizes[
            equivalence_class_sizes
            <
            k_required
        ]
    )


    # Đếm số nhóm chưa đạt yêu cầu k.
    so_nhom_vi_pham_k = len(
        violating_groups
    )


    # Cộng kích thước của tất cả nhóm vi phạm
    # để biết tổng số bản ghi đang vi phạm k.
    so_ban_ghi_vi_pham_k = int(
        violating_groups.sum()
    )


    # 8. TÍNH TỶ LỆ BẢN GHI VI PHẠM k

    if len(dataframe) == 0:

        ty_le_ban_ghi_vi_pham_k = 0.0

    else:

        ty_le_ban_ghi_vi_pham_k = (
            so_ban_ghi_vi_pham_k
            /
            len(dataframe)
            *
            100
        )


    # 9. KẾT LUẬN k-ANONYMITY

    # Dataset đạt yêu cầu k
    # nếu nhóm nhỏ nhất vẫn có ít nhất k_required bản ghi.
    #
    # Ví dụ:
    #
    # k_min = 5
    # k_required = 5
    #
    # → True
    k_valid = (
        k_min
        >=
        k_required
    )


    # 10. TRẢ KẾT QUẢ

    return {

        # Tổng số equivalence class
        "so_equivalence_class":
            so_equivalence_class,

        # Giá trị k nhỏ nhất thực tế
        "k_min":
            k_min,

        # Giá trị k mà hệ thống yêu cầu
        "k_required":
            k_required,

        # True nếu dataset đạt k-anonymity
        "k_valid":
            k_valid,

        # Số nhóm chỉ chứa đúng 1 bản ghi
        "so_nhom_1_ban_ghi":
            so_nhom_1_ban_ghi,

        # Số bản ghi bị cô lập
        "so_ban_ghi_bi_co_lap":
            so_ban_ghi_bi_co_lap,

        # Tỷ lệ bản ghi bị cô lập
        "ty_le_bi_co_lap_%":
            round(
                ty_le_bi_co_lap,
                2
            ),

        # Số equivalence class chưa đạt k
        "so_nhom_vi_pham_k":
            so_nhom_vi_pham_k,

        # Tổng số bản ghi nằm trong nhóm chưa đạt k
        "so_ban_ghi_vi_pham_k":
            so_ban_ghi_vi_pham_k,

        # Tỷ lệ bản ghi chưa đạt k
        "ty_le_ban_ghi_vi_pham_k_%":
            round(
                ty_le_ban_ghi_vi_pham_k,
                2
            ),

        # GIỮ CÁC KEY CŨ ĐỂ TƯƠNG THÍCH CODE TRƯỚC ĐÂY

        # Trước đây notebook của đồ án dùng tên key có "_k5".
        # Ta vẫn giữ chúng để code cũ không bị lỗi.
        #
        # Sau này nên ưu tiên dùng các key tổng quát phía trên.
        "so_nhom_vi_pham_k5":
            so_nhom_vi_pham_k,

        "so_ban_ghi_vi_pham_k5":
            so_ban_ghi_vi_pham_k,

        "ty_le_vi_pham_k5_%":
            round(
                ty_le_ban_ghi_vi_pham_k,
                2
            )
    }


# HÀM ĐÁNH GIÁ L-DIVERSITY


# Hàm evaluate_l_diversity() dùng để kiểm tra
# mức độ đa dạng của thuộc tính nhạy cảm
# bên trong từng equivalence class.
#
# Trong đồ án hiện tại:
#
# sensitive_column = "thu_nhap"
#
# Với l_required = 2,
# mỗi nhóm phải có ít nhất 2 giá trị thu_nhap khác nhau.
def evaluate_l_diversity(
    dataframe,
    qi_columns,
    sensitive_column,
    l_required=2
):

    # 1. KIỂM TRA ĐẦU VÀO
    # Không thể đánh giá l-diversity
    # nếu danh sách QI bị rỗng.
    if not qi_columns:

        raise ValueError(
            "Danh sách qi_columns không được để trống."
        )


    # Kiểm tra tất cả QI có tồn tại hay không.
    missing_qi_columns = [
        column
        for column in qi_columns
        if column not in dataframe.columns
    ]


    if missing_qi_columns:

        raise ValueError(
            f"Dataset thiếu các cột QI: {missing_qi_columns}"
        )


    # Kiểm tra cột nhạy cảm có tồn tại hay không.
    if sensitive_column not in dataframe.columns:

        raise ValueError(
            f"Dataset không có cột nhạy cảm '{sensitive_column}'."
        )


    # 2. TÍNH l CỦA TỪNG EQUIVALENCE CLASS

    # Gom dữ liệu theo các cột QI.
    #
    # Sau đó đếm số giá trị khác nhau
    # của thuộc tính nhạy cảm trong từng nhóm.
    #
    # Ví dụ:
    #
    # Nhóm A có:
    # <=50K
    # <=50K
    # >50K
    #
    # → nhóm A có l = 2.
    l_values = (

        dataframe

        .groupby(
            qi_columns,
            dropna=False
        )[sensitive_column]

        .nunique(
            dropna=False
        )
    )


    # 3. TÌM l NHỎ NHẤT

    # Nếu dataset rỗng
    # thì đặt l_min = 0.
    if l_values.empty:

        l_min = 0

    else:

        # Nhóm có độ đa dạng thấp nhất
        # quyết định l_min của toàn dataset.
        l_min = int(
            l_values.min()
        )


    # 4. ĐẾM SỐ EQUIVALENCE CLASS

    so_equivalence_class = len(
        l_values
    )


    # 5. ĐẾM SỐ NHÓM VI PHẠM l

    # Nhóm nào có:
    #
    # l < l_required
    #
    # sẽ bị xem là chưa đạt l-diversity.
    so_nhom_vi_pham_l = int(
        (
            l_values
            <
            l_required
        ).sum()
    )


    # 6. GẮN GIÁ TRỊ l CHO TỪNG BẢN GHI

    # Mỗi bản ghi sẽ nhận giá trị l
    # của equivalence class mà nó thuộc về.
    #
    # Dùng lambda để đảm bảo giá trị thiếu
    # cũng được tính giống cách tính l_values phía trên.
    l_value_per_record = (

        dataframe

        .groupby(
            qi_columns,
            dropna=False
        )[sensitive_column]

        .transform(
            lambda series:
            series.nunique(
                dropna=False
            )
        )
    )


    # 7. XÁC ĐỊNH BẢN GHI VI PHẠM l

    # True nghĩa là bản ghi đang nằm
    # trong equivalence class chưa đạt l_required.
    violation_mask = (
        l_value_per_record
        <
        l_required
    )


    # Đếm tổng số bản ghi vi phạm l.
    so_ban_ghi_vi_pham_l = int(
        violation_mask.sum()
    )


    # 8. TÍNH TỶ LỆ BẢN GHI VI PHẠM l

    # Tránh chia cho 0 nếu dataset rỗng.
    if len(dataframe) == 0:

        ty_le_ban_ghi_vi_pham_l = 0.0

    else:

        ty_le_ban_ghi_vi_pham_l = (
            so_ban_ghi_vi_pham_l
            /
            len(dataframe)
            *
            100
        )


    # 9. KẾT LUẬN l-DIVERSITY

    # Dataset đạt yêu cầu l
    # nếu nhóm có độ đa dạng thấp nhất
    # vẫn đạt ít nhất l_required.
    l_valid = (
        l_min
        >=
        l_required
    )


    # 10. TRẢ KẾT QUẢ

    return {

        # Tổng số equivalence class
        "so_equivalence_class":
            so_equivalence_class,

        # Giá trị l nhỏ nhất thực tế
        "l_min":
            l_min,

        # Giá trị l mà hệ thống yêu cầu
        "l_required":
            l_required,

        # True nếu toàn dataset đạt l-diversity
        "l_valid":
            l_valid,

        # Số nhóm chưa đạt l
        "so_nhom_vi_pham_l":
            so_nhom_vi_pham_l,

        # Số bản ghi nằm trong nhóm chưa đạt l
        "so_ban_ghi_vi_pham_l":
            so_ban_ghi_vi_pham_l,

        # Tỷ lệ bản ghi chưa đạt l
        "ty_le_ban_ghi_vi_pham_l_%":
            round(
                ty_le_ban_ghi_vi_pham_l,
                2
            )
    }


# HÀM ĐÁNH GIÁ PRIVACY TỔNG HỢP



def evaluate_privacy_full(
    dataframe,
    qi_columns,
    sensitive_column,
    k_required=5,
    l_required=2
):

    # 1. ĐÁNH GIÁ k-ANONYMITY

    k_result = evaluate_privacy(

        # Dataset cần đánh giá
        dataframe=dataframe,

        # Các cột Quasi-Identifier
        qi_columns=qi_columns,

        # Ngưỡng k của thực nghiệm
        k_required=k_required
    )


    # 2. ĐÁNH GIÁ l-DIVERSITY

    l_result = evaluate_l_diversity(

        # Dataset cần đánh giá
        dataframe=dataframe,

        # Các cột QI
        qi_columns=qi_columns,

        # Thuộc tính nhạy cảm
        sensitive_column=sensitive_column,

        # Ngưỡng l của thực nghiệm
        l_required=l_required
    )

    # 3. KIỂM TRA k CÓ ĐẠT KHÔNG

    # Có thể lấy trực tiếp k_valid
    # từ kết quả evaluate_privacy().
    k_valid = (
        k_result[
            "k_valid"
        ]
    )

    # 4. KIỂM TRA l CÓ ĐẠT KHÔNG
    # Lấy kết luận l_valid
    # từ evaluate_l_diversity().
    l_valid = (
        l_result[
            "l_valid"
        ]
    )

    # 5. KẾT LUẬN PRIVACY
    # Dataset chỉ được xem là đạt tiêu chí Privacy của đồ án
    # khi đồng thời:
    #
    # k_valid = True
    # và
    # l_valid = True
    privacy_valid = (
        k_valid
        and
        l_valid
    )

    # 6. TRẢ KẾT QUẢ TỔNG HỢP

    return {

        # Giá trị k nhỏ nhất thực tế
        "k_min":
            k_result[
                "k_min"
            ],

        # Ngưỡng k yêu cầu
        "k_required":
            k_required,

        # Kết luận k-anonymity
        "k_valid":
            k_valid,

        # Số bản ghi còn vi phạm k
        "so_ban_ghi_vi_pham_k":
            k_result[
                "so_ban_ghi_vi_pham_k"
            ],

        # Giá trị l nhỏ nhất thực tế
        "l_min":
            l_result[
                "l_min"
            ],

        # Ngưỡng l yêu cầu
        "l_required":
            l_required,

        # Kết luận l-diversity
        "l_valid":
            l_valid,

        # Số nhóm còn vi phạm l
        "so_nhom_vi_pham_l":
            l_result[
                "so_nhom_vi_pham_l"
            ],

        # Số bản ghi còn vi phạm l
        "so_ban_ghi_vi_pham_l":
            l_result[
                "so_ban_ghi_vi_pham_l"
            ],

        # Kết luận Privacy tổng hợp
        "privacy_valid":
            privacy_valid
    }

