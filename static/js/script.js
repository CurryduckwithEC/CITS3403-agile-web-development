$(function() {
    $(".like").click(function() {
        var $heartIcon = $(this);
        var postId = $heartIcon.data("post-id");
        var uncoloredSrc = "../static/images/aixin-2.png";
        var coloredSrc = "../static/images/aixin.png";

        $.post(`/toggle_like/${postId}`, function(data) {
            if (data.success) {
                if (data.liked) {
                    $heartIcon.attr("src", coloredSrc);
                } else {
                    $heartIcon.attr("src", uncoloredSrc);
                }
            } else {
                alert("Unable to toggle like status.");
            }
        });
    });
});
