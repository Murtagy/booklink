export class Worker {
  constructor(
    public worker_id: string,
    public name: string,
    public job_title: string,
    public display_description?: string
  ) {}
}
