#
# FILE: anonymization_engine.py
# Mục đích:
# Chứa các hàm thực hiện quá trình ẩn danh hóa dữ liệu,
# bao gồm Generalization, Suppression và chạy Candidate Strategy.


# HÀM GENERALIZATION TUỔI - STRATEGY AGE3


# Tạo hàm generalize_age_3 để chuyển tuổi cụ thể
# thành 3 khoảng tuổi rộng hơn nhằm giảm khả năng nhận diện cá nhân
def generalize_age_3(age):

    # Nếu tuổi nhỏ hơn hoặc bằng 49
    # thì đưa bản ghi vào nhóm tuổi 10-49
    if age <= 49:

        # Trả về nhóm tuổi 10-49
        return "10-49"

    # Nếu tuổi lớn hơn 49 nhưng nhỏ hơn hoặc bằng 69
    # thì đưa bản ghi vào nhóm tuổi 50-69
    elif age <= 69:

        # Trả về nhóm tuổi 50-69
        return "50-69"

    # Các tuổi còn lại sẽ thuộc nhóm 70-99
    else:

        # Trả về nhóm tuổi 70-99
        return "70-99"



# HÀM GENERALIZATION GIỜ LÀM VIỆC - STRATEGY HOURS3



# Tạo hàm generalize_hours_3 để chuyển số giờ làm việc cụ thể
# thành 3 khoảng giờ rộng hơn
def generalize_hours_3(hours):

    # Nếu số giờ làm việc nhỏ hơn hoặc bằng 40
    # thì đưa vào nhóm 1-40
    if hours <= 40:

        # Trả về nhóm giờ 1-40
        return "1-40"

    # Nếu số giờ lớn hơn 40 nhưng nhỏ hơn hoặc bằng 60
    # thì đưa vào nhóm 41-60
    elif hours <= 60:

        # Trả về nhóm giờ 41-60
        return "41-60"

    # Những trường hợp còn lại là trên 60 giờ
    else:

        # Trả về nhóm giờ 61-100
        return "61-100"



# HÀM GENERALIZATION HỌC VẤN - STRATEGY EDU3


# Tạo hàm generalize_education_3 để chuyển mức học vấn chi tiết
# thành 3 nhóm học vấn rộng hơn
#
# education_num:
#     Giá trị trong cột so_nam_hoc của dataset
#
# Lưu ý:
#     Trong dataset này, so_nam_hoc được dùng giống như
#     mã thứ bậc học vấn, không nên hiểu đơn giản là số năm học thực tế
def generalize_education_3(education_num):

    # Nếu mã học vấn nhỏ hơn hoặc bằng 9
    # thì gom vào nhóm THPT trở xuống
    if education_num <= 9:

        # Trả về nhóm học vấn THPT trở xuống
        return "THPT_tro_xuong"

    # Nếu mã học vấn từ 10 đến 12
    # thì gom vào nhóm sau THPT hoặc cao đẳng
    elif education_num <= 12:

        # Trả về nhóm sau THPT hoặc cao đẳng
        return "Sau_THPT_Cao_dang"

    # Các giá trị từ 13 trở lên
    # được gom vào nhóm đại học trở lên
    else:

        # Trả về nhóm đại học trở lên
        return "Dai_hoc_tro_len"



# HÀM GENERALIZATION TÌNH TRẠNG HÔN NHÂN - STRATEGY MARITAL2


# Tạo hàm generalize_marital_2 để chuyển tình trạng hôn nhân chi tiết
# thành 2 nhóm lớn hơn nhằm giảm mức độ chi tiết của QI
def generalize_marital_2(marital_status):

    # Tạo tập hợp chứa các trạng thái được xem là đã kết hôn
    married_statuses = {

        # Kết hôn dân sự
        "Ket_hon_dan_su",

        # Kết hôn nhưng vợ hoặc chồng đang vắng mặt
        "Ket_hon_vo_chong_vang_mat",

        # Kết hôn với quân nhân
        "Ket_hon_voi_quan_nhan"
    }

    # Nếu trạng thái hôn nhân nằm trong nhóm đã kết hôn
    if marital_status in married_statuses:

        # Gom thành nhóm Da_ket_hon
        return "Da_ket_hon"

    # Các trạng thái còn lại gồm:
    # Chua_ket_hon, Goa, Da_ly_hon và Ly_than
    else:

        # Gom thành nhóm không kết hôn hiện tại
        return "Khong_ket_hon_hien_tai"



# HÀM GENERALIZATION NGHỀ NGHIỆP - STRATEGY OCCUPATION4



# Tạo hàm generalize_occupation_4 để chuyển nghề nghiệp chi tiết
# thành 4 nhóm nghề nghiệp rộng hơn
def generalize_occupation_4(occupation):

    # Tạo nhóm nghề văn phòng, quản lý và chuyên môn
    office_professional = {

        # Nghề chuyên môn đặc thù
        "Chuyen_mon_dac_thu",

        # Công việc quản lý và điều hành
        "Quan_ly_dieu_hanh",

        # Nhân viên văn phòng
        "Nhan_vien_van_phong",

        # Công việc bán hàng
        "Ban_hang",

        # Công việc hỗ trợ kỹ thuật
        "Ho_tro_ky_thuat"
    }

    # Tạo nhóm nghề lao động trực tiếp
    manual_labor = {

        # Thợ thủ công và sửa chữa
        "Tho_thu_cong_sua_chua",

        # Công việc vận hành máy móc
        "Van_hanh_may_moc",

        # Công việc vận tải
        "Van_tai",

        # Công việc bốc xếp và dọn dẹp
        "Boc_xep_don_dep",

        # Công việc nông nghiệp và đánh bắt cá
        "Nong_nghiep_danh_bat_ca"
    }

    # Tạo nhóm nghề dịch vụ
    service_jobs = {

        # Các công việc dịch vụ khác
        "Dich_vu_khac",

        # Công việc bảo vệ
        "Dich_vu_bao_ve",

        # Giúp việc gia đình
        "Giup_viec_gia_dinh",

        # Công việc quân đội
        "Quan_doi"
    }

    # Nếu nghề thuộc nhóm văn phòng hoặc chuyên môn
    if occupation in office_professional:

        # Gom thành nhóm Van_phong_chuyen_mon
        return "Van_phong_chuyen_mon"

    # Nếu nghề thuộc nhóm lao động trực tiếp
    elif occupation in manual_labor:

        # Gom thành nhóm Lao_dong_truc_tiep
        return "Lao_dong_truc_tiep"

    # Nếu nghề thuộc nhóm dịch vụ
    elif occupation in service_jobs:

        # Gom thành nhóm Dich_vu
        return "Dich_vu"

    # Nếu dữ liệu gốc là dấu ?
    # nghĩa là chưa biết nghề nghiệp
    elif occupation == "?":

        # Gom thành nhóm Khong_ro
        return "Khong_ro"

    # Nếu giá trị là pd.NA hoặc một giá trị chưa biết khác
    # thì cũng đưa vào nhóm Khong_ro
    else:

        # Trả về nhóm không rõ
        return "Khong_ro"



# HÀM GENERALIZATION LOẠI CÔNG VIỆC - STRATEGY WORKCLASS5



# Tạo hàm generalize_workclass_5 để chuyển loại công việc chi tiết
# thành 5 nhóm rộng hơn
def generalize_workclass_5(workclass):

    # Tạo nhóm các công việc thuộc khu vực nhà nước
    government_classes = {

        # Chính quyền địa phương
        "Chinh_quyen_dia_phuong",

        # Chính quyền bang
        "Chinh_quyen_bang",

        # Chính phủ liên bang
        "Chinh_phu_lien_bang"
    }

    # Tạo nhóm các hình thức tự kinh doanh
    self_employed_classes = {

        # Tự kinh doanh không đăng ký
        "Tu_kinh_doanh_khong_dang_ky",

        # Tự kinh doanh có đăng ký
        "Tu_kinh_doanh_co_dang_ky"
    }

    # Tạo nhóm không lương hoặc chưa từng làm việc
    no_pay_classes = {

        # Công việc không lương
        "Khong_luong",

        # Chưa từng làm việc
        "Chua_tung_lam_viec"
    }

    # Nếu loại công việc là tư nhân
    if workclass == "Tu_nhan":

        # Giữ lại nhóm Tu_nhan
        return "Tu_nhan"

    # Nếu thuộc nhóm tự kinh doanh
    elif workclass in self_employed_classes:

        # Gom thành nhóm Tu_kinh_doanh
        return "Tu_kinh_doanh"

    # Nếu thuộc nhóm nhà nước
    elif workclass in government_classes:

        # Gom thành nhóm Nha_nuoc
        return "Nha_nuoc"

    # Nếu thuộc nhóm không lương hoặc chưa từng làm việc
    elif workclass in no_pay_classes:

        # Gom thành nhóm Khong_luong_hoac_chua_lam
        return "Khong_luong_hoac_chua_lam"

    # Nếu dữ liệu gốc là dấu ?
    # nghĩa là chưa biết loại công việc
    elif workclass == "?":

        # Gom thành nhóm Khong_ro
        return "Khong_ro"

    # Nếu giá trị là pd.NA hoặc một giá trị chưa biết khác
    # thì cũng đưa vào nhóm Khong_ro
    else:

        # Trả về nhóm không rõ
        return "Khong_ro"



# HÀM GENERALIZATION QUỐC GIA - STRATEGY COUNTRY2



# Tạo hàm generalize_country_2 để chuyển quốc gia chi tiết
# thành 2 nhóm rộng hơn
def generalize_country_2(country):

    # Tạo nhóm các giá trị được xem là thuộc Hoa_Ky
    usa_group = {

        # Quốc gia Hoa Kỳ
        "Hoa_Ky",

        # Lãnh thổ hải ngoại của Mỹ
        "Lanh_tho_hai_ngoai_My"
    }

    # Nếu quốc gia thuộc nhóm Hoa_Ky
    if country in usa_group:

        # Gom thành nhóm Hoa_Ky
        return "Hoa_Ky"

    # Các quốc gia còn lại, dấu ? hoặc giá trị không rõ
    # đều được gom chung vào một nhóm
    else:

        # Trả về nhóm các quốc gia khác hoặc không rõ
        return "Khac_hoac_khong_ro"



# HÀM ÁP DỤNG GENERALIZATION CHO TOÀN BỘ STRATEGY 1



# Tạo hàm apply_strategy_1_generalization để áp dụng đồng thời
# 7 phép generalization của Strategy 1 lên toàn bộ dataset
#
# dataframe:
#     DataFrame chứa dữ liệu gốc cần ẩn danh hóa
#
# Hàm này CHƯA thực hiện suppression
# mà mới chỉ tạo ra các cột QI đã được generalization
def apply_strategy_1_generalization(dataframe):

    # Tạo một bản sao của dữ liệu gốc
    # để không làm thay đổi trực tiếp DataFrame ban đầu
    generalized_data = dataframe.copy()

    # Generalization tuổi cụ thể thành 3 nhóm tuổi
    generalized_data["tuoi_nhom_3"] = (
        generalized_data["tuoi"]
        .apply(
            generalize_age_3
        )
    )

    # Generalization loại công việc thành 5 nhóm lớn
    generalized_data["loai_cong_viec_nhom"] = (
        generalized_data["loai_cong_viec"]
        .apply(
            generalize_workclass_5
        )
    )

    # Generalization học vấn dựa trên cột so_nam_hoc
    # thành 3 nhóm học vấn
    generalized_data["hoc_van_nhom_3"] = (
        generalized_data["so_nam_hoc"]
        .apply(
            generalize_education_3
        )
    )

    # Generalization tình trạng hôn nhân
    # thành 2 nhóm lớn
    generalized_data["hon_nhan_nhom_2"] = (
        generalized_data["tinh_trang_hon_nhan"]
        .apply(
            generalize_marital_2
        )
    )

    # Generalization nghề nghiệp
    # thành 4 nhóm nghề nghiệp
    generalized_data["nghe_nghiep_nhom_4"] = (
        generalized_data["nghe_nghiep"]
        .apply(
            generalize_occupation_4
        )
    )

    # Generalization số giờ làm việc mỗi tuần
    # thành 3 khoảng giờ
    generalized_data["gio_lam_nhom_3"] = (
        generalized_data["gio_lam_moi_tuan"]
        .apply(
            generalize_hours_3
        )
    )

    # Generalization quốc gia
    # thành Hoa_Ky hoặc Khac_hoac_khong_ro
    generalized_data["quoc_gia_nhom_2"] = (
        generalized_data["quoc_gia"]
        .apply(
            generalize_country_2
        )
    )

    # Trả về DataFrame đã có thêm 7 cột generalization
    # Các cột gốc vẫn được giữ lại để chúng ta còn kiểm tra
    return generalized_data


# HÀM SUPPRESSION ĐỂ ĐẠT K-ANONYMITY



# Tạo hàm suppress_k_anonymity để loại bỏ toàn bộ các bản ghi
# nằm trong equivalence class có kích thước nhỏ hơn k yêu cầu
#
# dataframe:
#     DataFrame đã được generalization
#
# qi_columns:
#     Danh sách các cột QI dùng để tạo equivalence class
#
# k_required:
#     Giá trị k tối thiểu mong muốn, mặc định là k=5
def suppress_k_anonymity(
    dataframe,
    qi_columns,
    k_required=5
):
    """
    Loại bỏ các bản ghi thuộc equivalence class
    có kích thước nhỏ hơn k_required.
    """

    # k phải là số nguyên dương.
    if not isinstance(k_required, int):
        raise TypeError(
            "k_required phải là số nguyên."
        )

    if k_required <= 0:
        raise ValueError(
            "k_required phải lớn hơn 0."
        )

    # Phải có ít nhất một QI.
    if not isinstance(qi_columns, (list, tuple)):
        raise TypeError(
            "qi_columns phải là list hoặc tuple."
        )

    if len(qi_columns) == 0:
        raise ValueError(
            "qi_columns không được để trống."
        )

    # Kiểm tra các cột QI có tồn tại không.
    missing_qi_columns = [
        column
        for column in qi_columns
        if column not in dataframe.columns
    ]

    if missing_qi_columns:
        raise ValueError(
            f"Thiếu các cột QI: {missing_qi_columns}"
        )

    # Tạo bản sao để không sửa trực tiếp dữ liệu đầu vào.
    suppressed_data = dataframe.copy()

    # Tính kích thước equivalence class của từng bản ghi.
    group_sizes = (
        suppressed_data
        .groupby(
            list(qi_columns),
            dropna=False
        )[qi_columns[0]]
        .transform(
            "size"
        )
    )

    # Chỉ giữ những bản ghi thuộc nhóm đạt k.
    keep_mask = (
        group_sizes
        >= k_required
    )

    suppressed_data = (
        suppressed_data
        .loc[
            keep_mask
        ]
        .copy()
    )

    # Không reset index vì index gốc còn dùng cho ML.
    return suppressed_data

# HÀM SUPPRESSION ĐỂ ĐẠT L-DIVERSITY



# Tạo hàm suppress_l_diversity để loại bỏ toàn bộ các bản ghi
# nằm trong equivalence class chưa đạt mức l-diversity yêu cầu
#
# dataframe:
#     DataFrame đã qua generalization và k-suppression
#
# qi_columns:
#     Danh sách các cột QI dùng để tạo equivalence class
#
# sensitive_column:
#     Cột nhạy cảm cần được bảo vệ, trong đồ án này là thu_nhap
#
# l_required:
#     Số lượng giá trị nhạy cảm khác nhau tối thiểu cần có trong mỗi nhóm
#     Strategy 1 của chúng ta sử dụng l=2
def suppress_l_diversity(
    dataframe,
    qi_columns,
    sensitive_column,
    l_required=2
):
    """
    Loại bỏ các equivalence class
    chưa đạt l-diversity yêu cầu.
    """

    # l phải là số nguyên dương.
    if not isinstance(l_required, int):
        raise TypeError(
            "l_required phải là số nguyên."
        )

    if l_required <= 0:
        raise ValueError(
            "l_required phải lớn hơn 0."
        )

    # Phải có ít nhất một QI.
    if not isinstance(qi_columns, (list, tuple)):
        raise TypeError(
            "qi_columns phải là list hoặc tuple."
        )

    if len(qi_columns) == 0:
        raise ValueError(
            "qi_columns không được để trống."
        )

    # Kiểm tra các cột QI.
    missing_qi_columns = [
        column
        for column in qi_columns
        if column not in dataframe.columns
    ]

    if missing_qi_columns:
        raise ValueError(
            f"Thiếu các cột QI: {missing_qi_columns}"
        )

    # Kiểm tra cột nhạy cảm.
    if sensitive_column not in dataframe.columns:
        raise KeyError(
            f"Column not found: {sensitive_column}"
        )

    # Tạo bản sao dữ liệu đầu vào.
    suppressed_data = dataframe.copy()

    # Tính số giá trị nhạy cảm khác nhau trong từng equivalence class.
    l_values = (
        suppressed_data
        .groupby(
            list(qi_columns),
            dropna=False
        )[sensitive_column]
        .transform(
            lambda series: series.nunique(dropna=False)
        )
    )

    # Chỉ giữ các nhóm đạt l-diversity.
    keep_mask = (
        l_values
        >= l_required
    )

    suppressed_data = (
        suppressed_data
        .loc[
            keep_mask
        ]
        .copy()
    )

    # Không reset index vì index gốc còn dùng cho ML.
    return suppressed_data


# HÀM CHẠY TOÀN BỘ QUY TRÌNH ẨN DANH HÓA STRATEGY 1


# Tạo hàm anonymize_strategy_1 để chạy toàn bộ Strategy 1
# từ dữ liệu gốc cho đến dữ liệu cuối cùng được phép phát hành
def anonymize_strategy_1(
    dataframe,
    k_required=5,
    l_required=2
):

    # Khai báo 7 cột QI sau generalization
    # Các cột này sẽ được dùng để tạo equivalence class
    qi_columns = [
        "tuoi_nhom_3",
        "loai_cong_viec_nhom",
        "hoc_van_nhom_3",
        "hon_nhan_nhom_2",
        "nghe_nghiep_nhom_4",
        "gio_lam_nhom_3",
        "quoc_gia_nhom_2"
    ]


    # Bước 1:
    # Áp dụng toàn bộ 7 phép generalization lên dữ liệu gốc
    generalized_data = apply_strategy_1_generalization(
        dataframe
    )


    # Bước 2:
    # Suppression các equivalence class có kích thước nhỏ hơn k yêu cầu
    data_after_k = suppress_k_anonymity(
        generalized_data,
        qi_columns,
        k_required=k_required
    )


    # Bước 3:
    # Suppression các equivalence class chưa đạt l-diversity yêu cầu
    data_after_l = suppress_l_diversity(
        data_after_k,
        qi_columns,
        sensitive_column="thu_nhap",
        l_required=l_required
    )


    # Khai báo các cột được phép giữ lại
    # trong dữ liệu ẩn danh cuối cùng
    release_columns = [
        "tuoi_nhom_3",
        "loai_cong_viec_nhom",
        "hoc_van_nhom_3",
        "hon_nhan_nhom_2",
        "nghe_nghiep_nhom_4",
        "gio_lam_nhom_3",
        "quoc_gia_nhom_2",
        "thu_nhap"
    ]


    # Chỉ giữ lại các cột đã được phép phát hành
    # Các cột chi tiết ban đầu sẽ không xuất hiện trong kết quả cuối cùng
    release_data = (
        data_after_l[
            release_columns
        ]
        .copy()
    )


    # Lấy lại index gốc của những bản ghi còn được giữ lại
    # Index này sau này dùng để lấy đúng các dòng tương ứng
    # trong dữ liệu gốc khi đánh giá Machine Learning
    retained_indices = (
        data_after_l
        .index
        .copy()
    )


    # Trả về:
    # 1. Dataset ẩn danh cuối cùng
    # 2. Index gốc của các bản ghi được giữ lại
    return release_data, retained_indices


# HÀM GENERALIZATION TUỔI - STRATEGY AGEHIGH


# Tạo hàm generalize_age_high để giữ tuổi chi tiết hơn Strategy 1
# bằng cách chia tuổi thành 4 nhóm thay vì 3 nhóm
#
# Hàm này sẽ được dùng cho Strategy 2
def generalize_age_high(age):

    # Nếu tuổi nhỏ hơn hoặc bằng 29
    # thì đưa vào nhóm tuổi 10-29
    if age <= 29:

        # Trả về nhóm tuổi 10-29
        return "10-29"

    # Nếu tuổi từ 30 đến 49
    # thì đưa vào nhóm tuổi 30-49
    elif age <= 49:

        # Trả về nhóm tuổi 30-49
        return "30-49"

    # Nếu tuổi từ 50 đến 69
    # thì đưa vào nhóm tuổi 50-69
    elif age <= 69:

        # Trả về nhóm tuổi 50-69
        return "50-69"

    # Các tuổi còn lại từ 70 trở lên
    # được gom vào nhóm 70-99
    else:

        # Trả về nhóm tuổi 70-99
        return "70-99"


# HÀM ÁP DỤNG GENERALIZATION CHO TOÀN BỘ STRATEGY 2



# Tạo hàm apply_strategy_2_generalization để áp dụng
# các phép generalization của Strategy 2 lên toàn bộ dataset
#
# Điểm khác chính so với Strategy 1:
# Strategy 2 sử dụng tuoi_nhom_high gồm 4 nhóm tuổi
# thay vì tuoi_nhom_3 gồm 3 nhóm tuổi
def apply_strategy_2_generalization(dataframe):

    # Tạo một bản sao của dữ liệu gốc
    # để không làm thay đổi trực tiếp DataFrame đầu vào
    generalized_data = dataframe.copy()


    # Generalization tuổi thành 4 nhóm của Strategy 2
    # Kết quả được lưu vào cột tuoi_nhom_high
    generalized_data["tuoi_nhom_high"] = (
        generalized_data["tuoi"]
        .apply(
            generalize_age_high
        )
    )


    # Generalization loại công việc thành 5 nhóm lớn
    # Phần này giống Strategy 1
    generalized_data["loai_cong_viec_nhom"] = (
        generalized_data["loai_cong_viec"]
        .apply(
            generalize_workclass_5
        )
    )


    # Generalization học vấn thành 3 nhóm
    # dựa trên cột so_nam_hoc
    generalized_data["hoc_van_nhom_3"] = (
        generalized_data["so_nam_hoc"]
        .apply(
            generalize_education_3
        )
    )


    # Generalization tình trạng hôn nhân thành 2 nhóm
    generalized_data["hon_nhan_nhom_2"] = (
        generalized_data["tinh_trang_hon_nhan"]
        .apply(
            generalize_marital_2
        )
    )


    # Generalization nghề nghiệp thành 4 nhóm
    generalized_data["nghe_nghiep_nhom_4"] = (
        generalized_data["nghe_nghiep"]
        .apply(
            generalize_occupation_4
        )
    )


    # Generalization số giờ làm việc thành 3 khoảng
    generalized_data["gio_lam_nhom_3"] = (
        generalized_data["gio_lam_moi_tuan"]
        .apply(
            generalize_hours_3
        )
    )


    # Generalization quốc gia thành 2 nhóm
    generalized_data["quoc_gia_nhom_2"] = (
        generalized_data["quoc_gia"]
        .apply(
            generalize_country_2
        )
    )


    # Trả về DataFrame đã được thêm 7 cột QI generalization
    # Các cột gốc vẫn được giữ lại để kiểm tra ở bước sau
    return generalized_data


# HÀM CHẠY TOÀN BỘ QUY TRÌNH ẨN DANH HÓA STRATEGY 2


# Tạo hàm anonymize_strategy_2 để chạy toàn bộ Strategy 2
# từ dữ liệu gốc đến dữ liệu cuối cùng được phép phát hành
def anonymize_strategy_2(
    dataframe,
    k_required=5,
    l_required=2
):

    # Khai báo 7 cột QI của Strategy 2
    # Điểm khác Strategy 1 là sử dụng tuoi_nhom_high
    qi_columns = [
        "tuoi_nhom_high",
        "loai_cong_viec_nhom",
        "hoc_van_nhom_3",
        "hon_nhan_nhom_2",
        "nghe_nghiep_nhom_4",
        "gio_lam_nhom_3",
        "quoc_gia_nhom_2"
    ]


    # Bước 1:
    # Áp dụng toàn bộ các phép generalization của Strategy 2
    generalized_data = apply_strategy_2_generalization(
        dataframe
    )


    # Bước 2:
    # Loại bỏ các bản ghi thuộc equivalence class có kích thước nhỏ hơn k
    data_after_k = suppress_k_anonymity(
        generalized_data,
        qi_columns,
        k_required=k_required
    )


    # Bước 3:
    # Loại bỏ các equivalence class chưa đạt l-diversity yêu cầu
    data_after_l = suppress_l_diversity(
        data_after_k,
        qi_columns,
        sensitive_column="thu_nhap",
        l_required=l_required
    )


    # Khai báo 8 cột được phép giữ lại
    # trong dataset phát hành cuối cùng của Strategy 2
    release_columns = [
        "tuoi_nhom_high",
        "loai_cong_viec_nhom",
        "hoc_van_nhom_3",
        "hon_nhan_nhom_2",
        "nghe_nghiep_nhom_4",
        "gio_lam_nhom_3",
        "quoc_gia_nhom_2",
        "thu_nhap"
    ]


    # Chỉ lấy các cột đã được phép phát hành
    # Không đưa các cột chi tiết ban đầu vào dataset cuối
    release_data = (
        data_after_l[
            release_columns
        ]
        .copy()
    )


    # Lấy lại index gốc của các bản ghi còn được giữ lại
    # Index này dùng để lấy đúng các dòng dữ liệu gốc
    # khi đánh giá Machine Learning
    retained_indices = (
        data_after_l
        .index
        .copy()
    )


    # Trả về:
    # 1. Dataset ẩn danh cuối cùng của Strategy 2
    # 2. Index gốc của các bản ghi được giữ lại
    return release_data, retained_indices


# HÀM CHỌN VÀ CHẠY STRATEGY THEO TÊN



# Tạo hàm anonymize_by_strategy để hệ thống có một điểm gọi chung
# thay vì phải gọi riêng anonymize_strategy_1() hoặc anonymize_strategy_2()
#
# dataframe:
#     Dataset gốc cần thực hiện ẩn danh hóa
#
# strategy_name:
#     Tên Strategy mà hệ thống muốn chạy
#
# k_required:
#     Giá trị k-anonymity yêu cầu
#
# l_required:
#     Giá trị l-diversity yêu cầu
def anonymize_by_strategy(
    dataframe,
    strategy_name,
    k_required=5,
    l_required=2
):

    # Nếu người dùng hoặc hệ thống yêu cầu Strategy 1
    if strategy_name == "strategy_1":

        # Gọi toàn bộ pipeline của Strategy 1
        return anonymize_strategy_1(
            dataframe,
            k_required=k_required,
            l_required=l_required
        )


    # Nếu người dùng hoặc hệ thống yêu cầu Strategy 2
    elif strategy_name == "strategy_2":

        # Gọi toàn bộ pipeline của Strategy 2
        return anonymize_strategy_2(
            dataframe,
            k_required=k_required,
            l_required=l_required
        )


    # Nếu strategy_name không phải Strategy 1 hoặc Strategy 2
    else:

        # Báo lỗi rõ ràng để tránh hệ thống âm thầm chạy sai Strategy
        raise ValueError(
            "strategy_name phải là 'strategy_1' hoặc 'strategy_2'"
        )

# GENERALIZATION GIỜ LÀM VIỆC - HOURS2


# Hàm này tổng quát hóa giờ làm việc thành 2 nhóm lớn hơn.
# hours2 sẽ mạnh hơn hours3 vì gộp toàn bộ các giá trị trên 40 giờ
# vào cùng một nhóm 41-100.
def generalize_hours_2(hours):

    # Nhóm giờ thông thường hoặc thấp hơn.
    if hours <= 40:
        return "1-40"

    # Nhóm giờ cao hơn 40 giờ mỗi tuần.
    else:
        return "41-100"



# HÀM LẤY CẤU HÌNH GENERALIZATION TUỔI CỦA CANDIDATE


def get_candidate_age_configuration(age_level):
    """
    Xác định hàm Generalization tuổi và tên cột tuổi đầu ra
    dựa trên age_level của Candidate.
    """

    # age3 tương ứng với 3 nhóm tuổi lớn.
    if age_level == "age3":
        return generalize_age_3, "tuoi_nhom_3"

    # age_high tương ứng với 4 nhóm tuổi chi tiết hơn.
    elif age_level == "age_high":
        return generalize_age_high, "tuoi_nhom_high"

    # Nếu cấu hình không hợp lệ thì dừng để tránh chạy sai Candidate.
    else:
        raise ValueError(
            "age_level phải là 'age3' hoặc 'age_high'."
        )



# HÀM LẤY CẤU HÌNH GENERALIZATION GIỜ LÀM VIỆC


def get_candidate_hours_configuration(hours_level):
    """
    Xác định hàm Generalization giờ làm việc và tên cột đầu ra
    dựa trên hours_level của Candidate.
    """

    # hours3 giữ cách chia cũ: 1-40, 41-60, 61-100.
    if hours_level == "hours3":
        return generalize_hours_3, "gio_lam_nhom_3"

    # hours2 tổng quát hóa mạnh hơn: 1-40, 41-100.
    elif hours_level == "hours2":
        return generalize_hours_2, "gio_lam_nhom_2"

    # Nếu cấu hình không hợp lệ thì báo lỗi rõ ràng.
    else:
        raise ValueError(
            "hours_level phải là 'hours3' hoặc 'hours2'."
        )


# HÀM TẠO DANH SÁCH QI CHO CANDIDATE


def get_candidate_qi_columns(strategy_config):
    """
    Tạo danh sách QI tương ứng với cấu hình Candidate Strategy.

    Candidate hiện thay đổi theo:
    - age_level
    - hours_level
    """

    # Cấu hình phải là dictionary.
    if not isinstance(strategy_config, dict):
        raise TypeError(
            "strategy_config phải là dictionary."
        )

    # Kiểm tra các key bắt buộc trước khi sử dụng.
    required_keys = [
        "age_level",
        "hours_level"
    ]

    for required_key in required_keys:
        if required_key not in strategy_config:
            raise ValueError(
                f"strategy_config thiếu key '{required_key}'."
            )

    # Lấy tên cột tuổi tương ứng với Candidate.
    _, age_column = get_candidate_age_configuration(
        strategy_config["age_level"]
    )

    # Lấy tên cột giờ làm việc tương ứng với Candidate.
    _, hours_column = get_candidate_hours_configuration(
        strategy_config["hours_level"]
    )

    # Tạo danh sách 7 QI sau Generalization.
    qi_columns = [
        age_column,
        "loai_cong_viec_nhom",
        "hoc_van_nhom_3",
        "hon_nhan_nhom_2",
        "nghe_nghiep_nhom_4",
        hours_column,
        "quoc_gia_nhom_2"
    ]

    return qi_columns


# HÀM GENERALIZATION THEO CẤU HÌNH CANDIDATE


def apply_candidate_generalization(dataframe, strategy_config):
    """
    Áp dụng Generalization theo cấu hình Candidate.

    Candidate hiện quyết định:
    - cách chia tuổi
    - cách chia giờ làm việc

    Các QI còn lại vẫn dùng mức Generalization cố định đã xây dựng.
    """

    # Kiểm tra cấu hình Candidate trước khi xử lý dữ liệu.
    if not isinstance(strategy_config, dict):
        raise TypeError(
            "strategy_config phải là dictionary."
        )

    required_keys = [
        "age_level",
        "hours_level"
    ]

    for required_key in required_keys:
        if required_key not in strategy_config:
            raise ValueError(
                f"strategy_config thiếu key '{required_key}'."
            )

    # Tạo bản sao để không làm thay đổi dataset gốc.
    generalized_data = dataframe.copy()

    # Lấy hàm và tên cột Generalization tuổi.
    age_function, age_column = get_candidate_age_configuration(
        strategy_config["age_level"]
    )

    # Lấy hàm và tên cột Generalization giờ làm việc.
    hours_function, hours_column = get_candidate_hours_configuration(
        strategy_config["hours_level"]
    )

    # Generalization tuổi theo cấu hình Candidate.
    generalized_data[age_column] = (
        generalized_data["tuoi"]
        .apply(age_function)
    )

    # Generalization loại công việc.
    generalized_data["loai_cong_viec_nhom"] = (
        generalized_data["loai_cong_viec"]
        .apply(generalize_workclass_5)
    )

    # Generalization học vấn.
    generalized_data["hoc_van_nhom_3"] = (
        generalized_data["so_nam_hoc"]
        .apply(generalize_education_3)
    )

    # Generalization tình trạng hôn nhân.
    generalized_data["hon_nhan_nhom_2"] = (
        generalized_data["tinh_trang_hon_nhan"]
        .apply(generalize_marital_2)
    )

    # Generalization nghề nghiệp.
    generalized_data["nghe_nghiep_nhom_4"] = (
        generalized_data["nghe_nghiep"]
        .apply(generalize_occupation_4)
    )

    # Generalization giờ làm việc theo cấu hình Candidate.
    generalized_data[hours_column] = (
        generalized_data["gio_lam_moi_tuan"]
        .apply(hours_function)
    )

    # Generalization quốc gia.
    generalized_data["quoc_gia_nhom_2"] = (
        generalized_data["quoc_gia"]
        .apply(generalize_country_2)
    )

    return generalized_data


# HÀM ẨN DANH HÓA MỘT CANDIDATE STRATEGY

def anonymize_candidate_strategy(
    dataframe,
    strategy_config,
    k_required=5,
    l_required=2
):
    """
    Chạy toàn bộ quy trình ẩn danh hóa theo Candidate Strategy:

    Generalization
        -> k-anonymity Suppression
        -> l-diversity Suppression
        -> Release Dataset
    """

    # Tạo danh sách QI đúng với Candidate hiện tại.
    qi_columns = get_candidate_qi_columns(
        strategy_config
    )

    # Bước 1: Generalization theo cấu hình Candidate.
    generalized_data = apply_candidate_generalization(
        dataframe=dataframe,
        strategy_config=strategy_config
    )

    # Bước 2: loại các equivalence class có kích thước nhỏ hơn k.
    data_after_k = suppress_k_anonymity(
        dataframe=generalized_data,
        qi_columns=qi_columns,
        k_required=k_required
    )

    # Bước 3: loại các equivalence class chưa đạt l-diversity.
    data_after_l = suppress_l_diversity(
        dataframe=data_after_k,
        qi_columns=qi_columns,
        sensitive_column="thu_nhap",
        l_required=l_required
    )

    # Dataset phát hành gồm 7 QI đã Generalization và cột nhạy cảm.
    release_columns = qi_columns + [
        "thu_nhap"
    ]

    # Chỉ giữ các cột được phép phát hành.
    release_data = (
        data_after_l[release_columns]
        .copy()
    )

    # Giữ index gốc để đối chiếu công bằng với dữ liệu Original khi đánh giá ML.
    retained_indices = (
        data_after_l
        .index
        .copy()
    )

    # Kiểm tra số dòng dữ liệu phát hành và số index phải khớp tuyệt đối.
    if len(release_data) != len(retained_indices):
        raise ValueError(
            "release_data và retained_indices không khớp."
        )

    return release_data, retained_indices


# KIỂM TRA CANDIDATE ENGINE KHI CHẠY FILE TRỰC TIẾP
# Phần kiểm tra này chỉ chạy khi bấm:
#
# Run anonymization_engine.py
#
# Khi pipeline.py import anonymization_engine
# thì đoạn này KHÔNG tự chạy.
if __name__ == "__main__":

    # IMPORT THƯ VIỆN CHỈ DÙNG CHO PHẦN TEST
    # Path dùng để xác định thư mục project.
    from pathlib import Path

    # pandas dùng để đọc dataset kiểm tra.
    import pandas as pd

    # Import module tự động sinh Candidate
    # nằm cùng thư mục src.
    import strategy_generator


    # XÁC ĐỊNH PROJECT ROOT


    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    # XÁC ĐỊNH DATASET

    dataset_file = (
        project_root
        / "data"
        / "dataset_anonymization.csv"
    )


    # Nếu dataset không tồn tại
    # thì dừng kiểm tra.
    if not dataset_file.exists():

        raise FileNotFoundError(
            f"Không tìm thấy dataset: {dataset_file}"
        )


    # ĐỌC DATASET

    test_data = (
        pd.read_csv(
            dataset_file
        )
    )


    # TỰ ĐỘNG SINH CANDIDATE

    candidate_strategies = (
        strategy_generator
        .generate_candidate_strategies()
    )


    print(
        "===== KIỂM TRA CANDIDATE ANONYMIZATION ENGINE ====="
    )


    print(
        "Số Candidate:",
        len(
            candidate_strategies
        )
    )


    # CHẠY TỪNG CANDIDATE

    for candidate in candidate_strategies:

        print(
            "\nCandidate:",
            candidate[
                "strategy_name"
            ]
        )


        print(
            "Age level:",
            candidate[
                "age_level"
            ]
        )


        # Hiển thị mức Generalization giờ làm việc của Candidate.
        print(
            "Hours level:",
            candidate[
                "hours_level"
            ]
        )


        # Chạy Candidate bằng engine mới.
        release_data, retained_indices = (
            anonymize_candidate_strategy(

                # Dataset gốc.
                dataframe=test_data,

                # Cấu hình Candidate.
                strategy_config=candidate,

                # Ngưỡng thực nghiệm của đồ án.
                k_required=5,

                # Ngưỡng thực nghiệm của đồ án.
                l_required=2
            )
        )


        # Hiển thị kích thước dữ liệu cuối.
        print(
            "Kích thước Release Data:",
            release_data.shape
        )


        # Hiển thị số retained indices.
        print(
            "Số retained indices:",
            len(
                retained_indices
            )
        )


        # Kiểm tra hai số liệu khớp nhau.
        print(
            "Release Data và retained indices khớp?:",
            len(
                release_data
            )
            ==
            len(
                retained_indices
            )
        )


        # Tính số bản ghi bị Suppression.
        suppressed_records = (
            len(
                test_data
            )
            -
            len(
                release_data
            )
        )


        # Tính tỷ lệ Suppression.
        suppression_percent = (
            suppressed_records
            /
            len(
                test_data
            )
            *
            100
        )


        print(
            "Suppressed records:",
            suppressed_records
        )


        print(
            "Suppression (%):",
            round(
                suppression_percent,
                2
            )
        )


    # THÔNG BÁO HOÀN THÀNH

    print(
        "\nCandidate Anonymization Engine: Chúc mừng bạn đã chạy thành công"
    )


