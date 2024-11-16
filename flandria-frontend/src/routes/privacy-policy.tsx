import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  homeBreadcrumbItems,
} from "@/components/page-header"

import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/privacy-policy")({
  component: () => (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Privacy policy", href: "/privacy-policy"},
          ]}
        />
        <PageTitle title="Privacy policy" />
      </PageHeader>
      <div className="prose">
        <p>
          At Flandria, your privacy is important to us. This Privacy Policy
          outlines the limited information we collect and how it is used. By
          using our website, you agree to the terms outlined below.
        </p>

        <h2>Information Collection and Use</h2>
        <p>
          We do not actively collect, store, or process personal information
          from our website visitors. The only data we collect is through
          standard server logs to monitor website performance and ensure
          security.
        </p>

        <h2>Server Logs</h2>
        <p>
          Like most websites, our server automatically records certain
          information, commonly referred to as logs, whenever you visit. These
          logs may include:
          <ul>
            <li>The date and time of your visit</li>
            <li>IP address (anonymized)</li>
            <li>
              Details of the enquiry and target address (log version, HTTP
              method, referrer, user agent string)
            </li>
            <li>
              Name of the file accessed and volume of data transferred (URL
              accessed including query string, size in bytes)
            </li>
            <li>
              Record of whether the query was successful (HTTP status code)
            </li>
          </ul>
          This information is used solely to analyze website traffic and
          performance, detect any potential security issues, and improve the
          overall user experience.
        </p>

        <h2>Data Retention</h2>
        <p>
          Logs are retained only as long as necessary for troubleshooting,
          analytics, and security purposes and are regularly purged to maintain
          your privacy.
        </p>

        <h2>Cookies</h2>
        <p>Flandria does not use any cookies.</p>

        <h2>Third-Party Services</h2>
        <p>
          We do not use any third-party services, cookies, or tracking
          technologies that collect personal data.
        </p>
        <h2>Your Privacy Rights</h2>
        <p>
          Since we do not collect personal data, there is no personal
          information to access, correct, or delete.
        </p>
      </div>
    </>
  ),
})
