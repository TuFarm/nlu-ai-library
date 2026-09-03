import { NavLink, Outlet, useLocation } from "react-router-dom";

const nav = [
  ["/admin", "⌂", "Tổng quan"], ["/kiosk", "▦", "Bảng thông tin"], ["/kiosk/face", "◎", "Nhận diện khuôn mặt"],
  ["/kiosk/chat", "✦", "Trợ lý AI"], ["/admin/knowledge", "▤", "Tài liệu tri thức"],
  ["/kiosk/books", "◇", "Gợi ý sách"], ["/kiosk/survey", "✓", "Khảo sát"], ["/admin/reports", "↗", "Báo cáo"],
];

export default function AppLayout() {
  const { pathname } = useLocation();
  const kioskMode = pathname.startsWith("/kiosk");
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">NL</span><div><strong>NLU Library</strong><small>AI Receptionist</small></div></div>
      <nav>{nav.map(([href, icon, label], index) => <NavLink key={href} to={href} end={href === "/admin" || href === "/kiosk"}>
        <span className="nav-icon">{icon}</span><span>{label}</span>{index > 1 && index < 5 && <i className="status-dot" title="Đang phát triển" />}
      </NavLink>)}</nav>
      <div className="sidebar-foot"><span className="online-dot" /> Hệ thống hoạt động<small>Phiên bản thử nghiệm 0.2</small></div>
    </aside>
    <section className="content-area">
      <header className="topbar"><div><span className="eyebrow">{kioskMode ? "CHẾ ĐỘ KIOSK" : "TRUNG TÂM QUẢN TRỊ"}</span><strong>Đại học Nông Lâm TP.HCM</strong></div><div className="top-actions"><span className="pill">● Mock data</span><div className="avatar">QT</div></div></header>
      <main className="page"><Outlet /></main>
    </section>
  </div>;
}
