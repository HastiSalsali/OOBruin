import logo from './00Bruin_logo.jpg'

export function Header() {
    return (
        <div className="Header">
            <img src={logo} alt="Logo" className="Header-logo" />
            <span className="Header-title">00Bruin</span>
        </div>
    )
}