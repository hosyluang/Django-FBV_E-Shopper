$(document).ready(function () {
    // Hien thi sao trung binh cho nguoi khac xem
    $('.ratings_stars').each(function (i) {
        if (i < activeRate) {
            $(this).addClass('ratings_over');
        }
    });

    // To lai sao ma user da chon
    // if (userRate > 0) {
    //     $('.ratings_stars').each(function () {
    //         let rateVal = $(this).find('input').val();
    //         if (rateVal <= userRate) {
    //             $(this).addClass('ratings_over');
    //         }
    //     });
    // }

    $('.ratings_stars').hover(
        function () {
            $(this).prevAll().andSelf().addClass('ratings_hover');
            // $(this).nextAll().removeClass('ratings_vote');
        },
        function () {
            $(this).prevAll().andSelf().removeClass('ratings_hover');
            // set_votes($(this).parent());
        },
    );

    // Khi click vao danh gia
    $('.ratings_stars').click(function () {
        if (isAuthenticated === 'true') {
            const rate = $(this).find('input').val();
            // console.log(rate);
            if ($(this).hasClass('ratings_over')) {
                $('.ratings_stars').removeClass('ratings_over');
                $(this).prevAll().andSelf().addClass('ratings_over');
            } else {
                $(this).prevAll().andSelf().addClass('ratings_over');
            }
            $.ajax({
                url: rateUrl,
                type: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                data: { rate: rate, id_blog: blogID },
                success: function (data) {
                    if (data.success) {
                        alert(`Cam on ban da danh gia ${rate} sao`);
                    } else {
                        console.log('Co loi xay ra:' + data.error);
                    }
                },
            });
        } else {
            alert('Yeu cau Login');
            window.location.href = `${loginUrl}?next={{ request.path }}`;
        }
    });

    // Khi click vao post comment
    $('#post_comment').click(function () {
        if (isAuthenticated !== 'true') {
            alert('Yêu cầu đăng nhập');
            window.location.href = `${loginUrl}?next={{ request.path }}`;
            return;
        }
        // Khi ko nhap cmt ma click
        const cmt = $('#comment_text').val().trim();
        if (cmt === '') {
            alert('Vui lòng nhập bình luận');
            return;
        }
        $.ajax({
            url: cmtUrl,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                id_blog: blogID,
                cmt: cmt,
            },
            success: function (res) {
                if (res.success) {
                    const data = res.data;
                    const createdAt = new Date(data.created_at);
                    const newCmt = `
                            <li class="media">
                                <a class="pull-left" href="#">
                                    <img class="media-object" src="${data.avatar_user}" alt="" width="80"/>
                                </a>
                                <div class="media-body">
                                    <ul class="sinlge-post-meta">
                                        <li><i class="fa fa-user"></i> ${data.name_user}</li>
                                        <li><i class="fa fa-clock-o"></i> ${createdAt.toLocaleTimeString()}</li>
                                        <li><i class="fa fa-calendar"></i> ${createdAt.toLocaleDateString()}</li>
                                    </ul>
                                    <p>${data.cmt}</p>
                                    <a class="btn btn-primary">
                                        <i class="fa fa-reply"></i> Reply
                                    </a>
                                </div>
                            </li>
                        `;
                    $('.media-list').append(newCmt);
                    // Xoa noi dung da nhap khi click
                    $('#comment_text').val('');
                    console.log('Đã thêm comment:', data);
                } else {
                    console.log(`Có lỗi xảy ra: ${res.error}`);
                }
            },
        });
    });

    // Khi click vao reply
    $('.reply-btn').click(function () {
        const id = $(this).data('id');
        console.log(id);
        $('#reply-form-' + id).toggle();
    });

    // Khi click submit reply
    $('.submit-reply').click(function () {
        if (isAuthenticated !== 'true') {
            alert('Yêu cầu đăng nhập');
            window.location.href = `${loginUrl}?next={{ request.path }}`;
            return;
        }
        const parent_id = $(this).data('id');
        console.log(parent_id);
        const replyCmt = $('#reply-form-' + parent_id + ' .reply-text').val();
        if (!replyCmt) return alert('Vui long nhap binh luan!');

        $.ajax({
            url: cmtUrl,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                id_blog: blogID,
                cmt: replyCmt,
                id_parent: parent_id,
            },
            success: function (res) {
                if (res.success) {
                    const data = res.data;
                    const createdAt = new Date(data.created_at);
                    const html = `
                        <li class="media second-media" id="comment-${data.id}">
                            <a class="pull-left" href="#">
                                <img class="media-object" src="${data.avatar_user}" alt="" width="80"/>
                            </a>
                            <div class="media-body">
                                <ul class="sinlge-post-meta">
                                    <li><i class="fa fa-user"></i> ${data.name_user}</li>
                                    <li><i class="fa fa-clock-o"></i> ${createdAt.toLocaleTimeString()}</li>
                                    <li><i class="fa fa-calendar"></i> ${createdAt.toLocaleDateString()}</li>
                                </ul>
                                <p>${data.cmt}</p>
                                <a class="btn btn-primary reply-btn" data-id="${data.id}">
                                    <i class="fa fa-reply"></i> Reply
                                </a>
                                <div class="reply-form " id="reply-form-${data.id}" style="display:none;">
                                    <textarea class="reply-text" rows="2" placeholder="Nhập bình luận..."></textarea>
                                    <button class="btn btn-success submit-reply" data-id="${data.id}">Gửi</button>
                                </div>
                            </div>
                        </li>
                    `;
                    $('#comment-' + parent_id).after(html);
                    $('#reply-form-' + parent_id + ' .reply-text').val('');
                    $('#reply-form-' + parent_id).toggle();
                }
            },
        });
    });
});
