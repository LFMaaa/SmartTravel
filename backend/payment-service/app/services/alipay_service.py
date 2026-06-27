"""
支付宝沙箱支付服务
使用 cryptography 库进行 RSA-SHA256 签名，生成支付宝电脑网站支付链接

支付宝沙箱配置（在 .env 中设置）：
  ALIPAY_APP_ID          — 沙箱应用 APPID
  ALIPAY_APP_PRIVATE_KEY — 应用私钥 (PKCS8 格式，一行，用 \n 表示换行)
  ALIPAY_PUBLIC_KEY      — 支付宝公钥
  ALIPAY_NOTIFY_URL      — 异步通知地址 (必须外网可访问)
  ALIPAY_RETURN_URL      — 同步跳转地址
"""

import os
import time
import base64
import logging
from typing import Optional
from urllib.parse import quote

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger("smarttravel.payment.alipay")

# ── 支付宝沙箱配置 ──────────────────────────────────────────────
ALIPAY_GATEWAY = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"  # 沙箱网关
ALIPAY_APP_ID = os.getenv("ALIPAY_APP_ID", "")
ALIPAY_NOTIFY_URL = os.getenv("ALIPAY_NOTIFY_URL", "http://localhost/api/v1/payment/member/alipay-notify")
ALIPAY_RETURN_URL = os.getenv("ALIPAY_RETURN_URL", "http://localhost/user/member?paid=1")
SIGN_TYPE = "RSA2"
CHARSET = "utf-8"

# ── 密钥从独立 PEM 文件加载（避免 .env 多行解析问题）───────────
_KEY_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _load_pem(filename: str) -> str:
    """从 payment-service 目录下加载 PEM 密钥文件"""
    path = os.path.join(_KEY_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

ALIPAY_APP_PRIVATE_KEY = _load_pem("alipay_private_key.pem")
ALIPAY_PUBLIC_KEY = _load_pem("alipay_public_key.pem")


def _is_configured() -> bool:
    """检查支付宝是否已配置"""
    return bool(ALIPAY_APP_ID and ALIPAY_APP_PRIVATE_KEY and ALIPAY_PUBLIC_KEY)


def _sign(data: str) -> str:
    """RSA2-SHA256 签名"""
    private_key = serialization.load_pem_private_key(
        ALIPAY_APP_PRIVATE_KEY.encode("utf-8"),
        password=None,
        backend=default_backend(),
    )
    signature = private_key.sign(
        data.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("utf-8")


def _verify(data: str, sign: str) -> bool:
    """验证支付宝回调签名"""
    public_key = serialization.load_pem_public_key(
        ALIPAY_PUBLIC_KEY.encode("utf-8"),
        backend=default_backend(),
    )
    try:
        public_key.verify(
            base64.b64decode(sign),
            data.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def build_pay_url(
    out_trade_no: str,
    total_amount: float,
    subject: str,
    body: Optional[str] = None,
    return_url: Optional[str] = None,
) -> Optional[str]:
    """
    构建支付宝电脑网站支付 URL

    参数:
      out_trade_no: 商户订单号 (即 order.id)
      total_amount: 支付金额 (元)
      subject: 商品标题
      body: 商品描述
      return_url: 同步跳转地址（不传则用 .env 中的默认值）

    返回:
      支付宝支付页面 URL，未配置时返回 None
    """
    if not _is_configured():
        logger.warning("支付宝未配置 (缺少 ALIPAY_APP_ID / ALIPAY_APP_PRIVATE_KEY)，无法生成支付链接")
        return None

    import json

    biz_content = {
        "out_trade_no": out_trade_no,
        "product_code": "FAST_INSTANT_TRADE_PAY",  # 电脑网站支付产品码
        "total_amount": f"{total_amount:.2f}",
        "subject": subject,
    }
    if body:
        biz_content["body"] = body

    params = {
        "app_id": ALIPAY_APP_ID,
        "method": "alipay.trade.page.pay",
        "charset": CHARSET,
        "sign_type": SIGN_TYPE,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "version": "1.0",
        "notify_url": ALIPAY_NOTIFY_URL,
        "return_url": return_url or ALIPAY_RETURN_URL,
        "biz_content": json.dumps(biz_content, ensure_ascii=False),
    }

    # 构建待签名字符串: key=value 按字母排序，用 & 连接
    sign_content = "&".join(
        f"{k}={params[k]}" for k in sorted(params.keys())
    )
    params["sign"] = _sign(sign_content)

    # 构建完整的支付 URL
    query_string = "&".join(
        f"{k}={quote(str(v), safe='')}" for k, v in params.items()
    )
    return f"{ALIPAY_GATEWAY}?{query_string}"


def verify_notify(params: dict) -> bool:
    """
    验证支付宝异步通知签名

    参数:
      params: POST 请求的所有参数 (dict)

    返回:
      签名是否有效
    """
    if not _is_configured():
        return False

    # 移除 sign 和 sign_type，其余排序拼接
    sign = params.pop("sign", "")
    params.pop("sign_type", None)

    sign_content = "&".join(
        f"{k}={params[k]}" for k in sorted(params.keys())
    )
    return _verify(sign_content, sign)
