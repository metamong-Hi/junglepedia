from flask import Blueprint, jsonify

logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/api/v1/logout', methods=['POST'])
def logout():
    # JWT 기반 인증 시스템에서 로그아웃은 프론트엔드에서 토큰을 삭제하는 것으로 처리됩니다.
    # 따라서 서버에서는 특별한 작업을 할 필요가 없으며, 단순히 성공 메시지를 반환하면 됩니다.
    return jsonify({"status": "success"}), 200
