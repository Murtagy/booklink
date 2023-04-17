import dayjs from "dayjs";
import type { OutVisitExtended } from "./client";


export function extended_visit_repr(visit: OutVisitExtended): string {
    const services_repr = visit.services.map((s) => s.name).join(', ')
    const worker_repr = visit.worker.name
    const time_repr = dayjs(visit.visit.from_datetime).format('YYYY/MM/DD HH:mm')
    return `${time_repr} ${services_repr} ${worker_repr}`
}