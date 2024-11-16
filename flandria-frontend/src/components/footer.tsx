import {Link} from "@tanstack/react-router"

export function Footer() {
  return (
    <footer className="flex flex-col items-center justify-around space-y-4 border-t bg-background px-10 pb-4 pt-6 text-sm md:flex-row md:space-y-0">
      <div className="flex items-center space-x-3">
        <img src="/full_logo_small.png" className="border-r pr-3" />
        <p className="max-w-xs">
          All information is provided as is, without guarantee of accuracy or
          currency.
        </p>
      </div>

      <div className="flex space-x-10">
        <div>
          <h3 className="font-semibold uppercase">Community</h3>
          <ul>
            <li>
              <a href="https://discord.gg/giikugames">Florensia Discord</a>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="font-semibold uppercase">Legal</h3>
          <ul className="gap-x-1 md:grid md:grid-cols-2">
            <li>
              <a
                target="_blank"
                href="https://www.giikugames.com/legal_disclosure.html"
              >
                Legal notice
              </a>
            </li>
            <li>
              <Link to="/copyright">Copyright</Link>
            </li>
            <li>
              <Link to="/privacy-policy">Privacy policy</Link>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  )
}
