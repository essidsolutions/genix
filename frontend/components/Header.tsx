import Link from "next/link";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import styles from "../styles/Header.module.css";

export default function Header() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const user = localStorage.getItem("user");
    setIsLoggedIn(!!user);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setIsLoggedIn(false);
    router.push("/");
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>Cloud Cost Optimizer</div>
      <div className={styles.links}>
        <Link href="/">Home</Link>
        {!isLoggedIn ? (
          <>
            <Link href="/auth/login">Login</Link>
            <Link href="/auth/signup">Sign Up</Link>
          </>
        ) : (
          <button className={styles.logout} onClick={handleLogout}>Logout</button>
        )}
      </div>
    </nav>
  );
}