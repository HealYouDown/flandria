import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  homeBreadcrumbItems,
} from "@/components/page-header"

import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/copyright")({
  component: () => (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Copyright", href: "/copyright"},
          ]}
        />
        <PageTitle title="Copyright Disclaimer" />
      </PageHeader>
      <div className="prose">
        <p>
          All images, data, and other content displayed on this website related
          to Florensia are the intellectual property of GiikuGames GmbH. They
          are used here for informational and community purposes only, without
          any claim to ownership.
        </p>
        <p>
          GiikuGames GmbH retains all rights, title, and interest in their
          respective assets, and no part of this website should be construed as
          infringing upon those rights.
        </p>
        <p>
          For more information about Florensia and GiikuGames GmbH, please visit
          the official Florensia website.
        </p>
      </div>
    </>
  ),
})
