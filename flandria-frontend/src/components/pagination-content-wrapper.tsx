export function PaginationContentWrapper({
  children,
}: React.ComponentProps<"div">) {
  return <div className="flex flex-col gap-4">{children}</div>
}
