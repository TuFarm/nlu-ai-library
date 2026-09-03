import type { ReactNode } from "react";
import { Link } from "react-router-dom";

export function PageHeader({ eyebrow, title, description, action }: { eyebrow?: string; title: string; description: string; action?: ReactNode }) {
  return <div className="page-header"><div>{eyebrow && <span className="eyebrow">{eyebrow}</span>}<h1>{title}</h1><p>{description}</p></div>{action}</div>;
}
export function StatusBadge({ status }: { status: string }) {
  const tone = status === "processed" ? "success" : status === "failed" ? "danger" : "warning";
  const label = status === "processed" ? "Đã xử lý" : status === "failed" ? "Lỗi xử lý" : status === "processing" ? "Đang xử lý" : status;
  return <span className={`badge ${tone}`}>{label}</span>;
}
export function MetricCard({ icon, label, value, detail }: { icon: string; label: string; value: string; detail: string }) {
  return <article className="metric-card"><span className="metric-icon">{icon}</span><div><p>{label}</p><strong>{value}</strong><small>{detail}</small></div></article>;
}
export function UnderDevelopmentCard({ title, description, backHref = "/kiosk", backLabel = "Về Bảng thông tin" }: { title: string; description?: string; backHref?: string; backLabel?: string }) {
  return <section className="development-card"><div className="development-icon">⌁</div><span className="badge warning">Đang phát triển</span><h2>{title}</h2><p>{description ?? "Chức năng đang phát triển và sẽ sớm hoàn thiện, bạn vui lòng chờ thêm một thời gian."}</p><small>Trong thời gian chờ, bạn có thể liên hệ trực tiếp bộ phận phụ trách nếu cần hỗ trợ.</small><Link className="button secondary" to={backHref}>← {backLabel}</Link></section>;
}
