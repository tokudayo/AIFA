const callbacks: { [key: string]: any } = {};
const eventBus = {
  // eslint-disable-next-line
  on(event: string, callback: any): void {
    callbacks[event] = (e: any) => callback(e.detail);
    document.addEventListener(event, callbacks[event]);
  },
  // eslint-disable-next-line
  dispatch(event: string, data: any): void {
    document.dispatchEvent(new CustomEvent(event, { detail: data }));
  },
  remove(event: string, callback: any = undefined): void {
    if (callback) {
      document.removeEventListener(event, callback);
    } else {
      document.removeEventListener(event, callbacks[event]);
    }
  },
};

export default eventBus;
