import tkinter as tk

from tkinter import ttk, messagebox

import threading

import queue

import pandas as pd

import os

import subprocess

import sys





from sequential_crawler import crawl_sequential

from parallel_crawler import crawl_parallel

from generate_pages import generate_pages



# ==========================================================

# FILE CONFIGURATION

# ==========================================================



GUI_RESULTS_FILE = "results/gui_performance_results.csv"






# ==========================================================

# MAIN GUI CLASS

# ==========================================================



class CrawlerGUI:



    def __init__(self, root):



        self.root = root



        self.root.title(

            "Parallel Web Crawler - Performance Dashboard"

        )



        self.root.geometry(

            "1150x900"

        )



        self.root.minsize(

            900,

            650

        )



        # --------------------------------------------------

        # Thread-safe result queue

        # --------------------------------------------------



        self.result_queue = queue.Queue()



        # --------------------------------------------------

        # Current results

        # --------------------------------------------------



        self.sequential_time = None
        self.sequential_pages = None
        self.parallel_time = None
        self.parallel_pages = None
        self.parallel_workers = None
        self.current_pages = None



        # ==================================================

        # SCROLLABLE WINDOW

        # ==================================================



        self.canvas = tk.Canvas(

            root,

            highlightthickness=0

        )



        self.scrollbar = ttk.Scrollbar(

            root,

            orient="vertical",

            command=self.canvas.yview

        )



        self.canvas.configure(

            yscrollcommand=self.scrollbar.set

        )



        self.scrollbar.pack(

            side="right",

            fill="y"

        )



        self.canvas.pack(

            side="left",

            fill="both",

            expand=True

        )



        self.main_frame = tk.Frame(

            self.canvas

        )



        self.canvas_window = self.canvas.create_window(

            (0, 0),

            window=self.main_frame,

            anchor="nw"

        )



        self.main_frame.bind(

            "<Configure>",

            self.update_scroll_region

        )



        self.canvas.bind(

            "<Configure>",

            self.resize_canvas

        )



        self.canvas.bind_all(

            "<MouseWheel>",

            self.mouse_scroll

        )



        # ==================================================

        # HEADER

        # ==================================================



        header = tk.Frame(

            self.main_frame,

            pady=25

        )



        header.pack(

            fill="x"

        )



        tk.Label(

            header,

            text="PARALLEL WEB CRAWLER",

            font=("Arial", 30, "bold")

        ).pack()



        tk.Label(

            header,

            text="Large-Scale Data Collection using Parallel Processing",

            font=("Arial", 14)

        ).pack(

            pady=8

        )



        # ==================================================

        # CONFIGURATION

        # ==================================================



        config_frame = tk.LabelFrame(

            self.main_frame,

            text="Crawler Configuration",

            font=("Arial", 15, "bold"),

            padx=35,

            pady=25

        )



        config_frame.pack(

            padx=60,

            pady=15,

            fill="x"

        )



        # --------------------------------------------------

        # START URL

        # --------------------------------------------------



        tk.Label(

            config_frame,

            text="Start URL:",

            font=("Arial", 12)

        ).grid(

            row=0,

            column=0,

            padx=15,

            pady=12,

            sticky="w"

        )



        self.url_entry = tk.Entry(

            config_frame,

            width=75,

            font=("Arial", 11)

        )



        self.url_entry.insert(

            0,

            "http://localhost:8000/page1.html"

        )



        self.url_entry.grid(

            row=0,

            column=1,

            padx=15,

            pady=12

        )



        # --------------------------------------------------

        # NUMBER OF PAGES

        # --------------------------------------------------



        tk.Label(

            config_frame,

            text="Number of Pages:",

            font=("Arial", 12)

        ).grid(

            row=1,

            column=0,

            padx=15,

            pady=12,

            sticky="w"

        )



        self.pages_entry = tk.Entry(

            config_frame,

            width=20,

            font=("Arial", 11)

        )



        self.pages_entry.insert(

            0,

            "50"

        )



        self.pages_entry.grid(

            row=1,

            column=1,

            padx=15,

            pady=12,

            sticky="w"

        )



        # --------------------------------------------------

        # WORKERS

        # --------------------------------------------------



        tk.Label(

            config_frame,

            text="Parallel Workers:",

            font=("Arial", 12)

        ).grid(

            row=2,

            column=0,

            padx=15,

            pady=12,

            sticky="w"

        )



        self.workers_combo = ttk.Combobox(

            config_frame,

            values=[2, 4, 8],

            width=17,

            state="readonly",

            font=("Arial", 11)

        )



        self.workers_combo.set(

            4

        )



        self.workers_combo.grid(

            row=2,

            column=1,

            padx=15,

            pady=12,

            sticky="w"

        )



        # ==================================================

        # BUTTONS

        # ==================================================



        button_frame = tk.Frame(

            self.main_frame,

            pady=15

        )



        button_frame.pack()



        self.generate_button = tk.Button(

            button_frame,

            text="GENERATE TEST PAGES",

            font=("Arial", 12, "bold"),

            padx=25,

            pady=14,

            command=self.generate_test_pages

        )



        self.generate_button.grid(

            row=0,

            column=0,

            padx=8

        )



        self.sequential_button = tk.Button(

            button_frame,

            text="RUN SEQUENTIAL",

            font=("Arial", 12, "bold"),

            padx=30,

            pady=14,

            command=self.run_sequential

        )



        self.sequential_button.grid(

            row=0,

            column=1,

            padx=8

        )



        self.parallel_button = tk.Button(

            button_frame,

            text="RUN PARALLEL",

            font=("Arial", 12, "bold"),

            padx=30,

            pady=14,

            command=self.run_parallel

        )



        self.parallel_button.grid(

            row=0,

            column=2,

            padx=8

        )



        self.clear_button = tk.Button(

            button_frame,

            text="CLEAR CURRENT",

            font=("Arial", 12, "bold"),

            padx=25,

            pady=14,

            command=self.clear_current

        )



        self.clear_button.grid(

            row=0,

            column=3,

            padx=8

        )



        # ==================================================

        # STATUS

        # ==================================================



        self.status_label = tk.Label(

            self.main_frame,

            text="Ready",

            font=("Arial", 12, "bold")

        )



        self.status_label.pack(

            pady=10

        )



        # ==================================================

        # CURRENT RUN RESULTS

        # ==================================================



        current_frame = tk.LabelFrame(

            self.main_frame,

            text="CURRENT RUN RESULTS",

            font=("Arial", 15, "bold"),

            padx=25,

            pady=25

        )



        current_frame.pack(

            padx=60,

            pady=15,

            fill="x"

        )



        # --------------------------------------------------

        # SEQUENTIAL

        # --------------------------------------------------



        seq_frame = tk.LabelFrame(

            current_frame,

            text="SEQUENTIAL CRAWLER",

            font=("Arial", 12, "bold"),

            padx=25,

            pady=20

        )



        seq_frame.grid(

            row=0,

            column=0,

            padx=15

        )



        tk.Label(

            seq_frame,

            text="Pages Crawled",

            font=("Arial", 11)

        ).grid(

            row=0,

            column=0,

            padx=30

        )



        self.seq_pages_label = tk.Label(

            seq_frame,

            text="-",

            font=("Arial", 24, "bold")

        )



        self.seq_pages_label.grid(

            row=1,

            column=0,

            padx=30

        )



        tk.Label(

            seq_frame,

            text="Execution Time",

            font=("Arial", 11)

        ).grid(

            row=0,

            column=1,

            padx=30

        )



        self.seq_time_label = tk.Label(

            seq_frame,

            text="-",

            font=("Arial", 24, "bold")

        )



        self.seq_time_label.grid(

            row=1,

            column=1,

            padx=30

        )



        # --------------------------------------------------

        # PARALLEL

        # --------------------------------------------------



        par_frame = tk.LabelFrame(

            current_frame,

            text="PARALLEL CRAWLER",

            font=("Arial", 12, "bold"),

            padx=25,

            pady=20

        )



        par_frame.grid(

            row=0,

            column=1,

            padx=15

        )



        tk.Label(

            par_frame,

            text="Pages Crawled",

            font=("Arial", 11)

        ).grid(

            row=0,

            column=0,

            padx=20

        )



        self.par_pages_label = tk.Label(

            par_frame,

            text="-",

            font=("Arial", 24, "bold")

        )



        self.par_pages_label.grid(

            row=1,

            column=0,

            padx=20

        )



        tk.Label(

            par_frame,

            text="Execution Time",

            font=("Arial", 11)

        ).grid(

            row=0,

            column=1,

            padx=20

        )



        self.par_time_label = tk.Label(

            par_frame,

            text="-",

            font=("Arial", 24, "bold")

        )



        self.par_time_label.grid(

            row=1,

            column=1,

            padx=20

        )



        tk.Label(

            par_frame,

            text="Workers",

            font=("Arial", 11)

        ).grid(

            row=0,

            column=2,

            padx=20

        )



        self.par_workers_label = tk.Label(

            par_frame,

            text="-",

            font=("Arial", 24, "bold")

        )



        self.par_workers_label.grid(

            row=1,

            column=2,

            padx=20

        )



        # ==================================================

        # CURRENT PERFORMANCE

        # ==================================================



        metric_frame = tk.LabelFrame(

            self.main_frame,

            text="CURRENT PERFORMANCE",

            font=("Arial", 15, "bold"),

            padx=30,

            pady=25

        )



        metric_frame.pack(

            padx=60,

            pady=15,

            fill="x"

        )



        speed_box = tk.Frame(

            metric_frame,

            padx=100

        )



        speed_box.grid(

            row=0,

            column=0

        )



        tk.Label(

            speed_box,

            text="SPEEDUP",

            font=("Arial", 13, "bold")

        ).pack()



        self.speedup_label = tk.Label(

            speed_box,

            text="-",

            font=("Arial", 30, "bold")

        )



        self.speedup_label.pack(

            pady=8

        )



        efficiency_box = tk.Frame(

            metric_frame,

            padx=100

        )



        efficiency_box.grid(

            row=0,

            column=1

        )



        tk.Label(

            efficiency_box,

            text="EFFICIENCY",

            font=("Arial", 13, "bold")

        ).pack()



        self.efficiency_label = tk.Label(

            efficiency_box,

            text="-",

            font=("Arial", 30, "bold")

        )



        self.efficiency_label.pack(

            pady=8

        )



        # ==================================================

        # DYNAMIC BENCHMARK

        # ==================================================



        benchmark_frame = tk.LabelFrame(

            self.main_frame,

            text="LIVE PERFORMANCE BENCHMARK",

            font=("Arial", 15, "bold"),

            padx=20,

            pady=20

        )



        benchmark_frame.pack(

            padx=60,

            pady=15,

            fill="x"

        )



        columns = (

            "pages",

            "method",

            "workers",

            "seqtime",

            "partime",

            "speedup",

            "efficiency"

        )



        self.table = ttk.Treeview(

            benchmark_frame,

            columns=columns,

            show="headings",

            height=8

        )



        headings = {

            "pages": "Pages",

            "method": "Method",

            "workers": "Workers",

            "seqtime": "Sequential (s)",

            "partime": "Parallel (s)",

            "speedup": "Speedup",

            "efficiency": "Efficiency (%)"

        }



        for column in columns:



            self.table.heading(

                column,

                text=headings[column]

            )



            self.table.column(

                column,

                width=125,

                anchor="center"

            )



        self.table.pack(

            fill="x"

        )



        # ==================================================
        # ==================================================

        # PROJECT INFORMATION

        # ==================================================



        info_frame = tk.LabelFrame(

            self.main_frame,

            text="Project Information",

            font=("Arial", 15, "bold"),

            padx=30,

            pady=25

        )



        info_frame.pack(

            padx=60,

            pady=15,

            fill="x"

        )



        info = (

            "Sequential Crawling\n"

            "• Processes webpages one after another.\n"

            "• Used as the performance baseline.\n\n"

            "Parallel Crawling\n"

            "• Uses multiple worker threads.\n"

            "• Multiple webpages are fetched concurrently.\n\n"

            "The live benchmark is stored in:\n"

            "results/gui_performance_results.csv"

        )



        tk.Label(

            info_frame,

            text=info,

            font=("Arial", 11),

            justify="left"

        ).pack(

            anchor="w"

        )



        # ==================================================

        # LOAD EXISTING RESULTS

        # ==================================================



        self.load_gui_results()



        # ==================================================

        # START QUEUE CHECKER

        # ==================================================



        self.root.after(

            100,

            self.process_queue

        )



    # ======================================================

    # SCROLLING

    # ======================================================



    def update_scroll_region(

        self,

        event=None

    ):



        self.canvas.configure(

            scrollregion=self.canvas.bbox("all")

        )



    def resize_canvas(

        self,

        event

    ):



        self.canvas.itemconfig(

            self.canvas_window,

            width=event.width

        )



    def mouse_scroll(

        self,

        event

    ):



        self.canvas.yview_scroll(

            int(

                -1 *

                (event.delta / 120)

            ),

            "units"

        )



    # ======================================================

    # QUEUE PROCESSOR

    # ======================================================



    def process_queue(self):



        try:



            while True:



                message = self.result_queue.get_nowait()



                message_type = message[0]



                # ------------------------------------------

                # STATUS

                # ------------------------------------------



                if message_type == "status":



                    self.status_label.config(

                        text=message[1]

                    )



                # ------------------------------------------

                # GENERATE COMPLETE

                # ------------------------------------------



                elif message_type == "generate_done":



                    pages = message[1]



                    self.status_label.config(

                        text=f"{pages} test pages generated successfully."

                    )



                    self.enable_buttons()



                # ------------------------------------------

                # GENERATE ERROR

                # ------------------------------------------



                elif message_type == "generate_error":



                    self.enable_buttons()



                    messagebox.showerror(

                        "Generation Error",

                        message[1]

                    )



                # ------------------------------------------

                # SEQUENTIAL COMPLETE

                # ------------------------------------------



                elif message_type == "sequential_done":



                    pages = message[1]

                    execution_time = message[2]



                    self.update_sequential(

                        pages,

                        execution_time

                    )



                    self.enable_buttons()



                # ------------------------------------------

                # SEQUENTIAL ERROR

                # ------------------------------------------



                elif message_type == "sequential_error":



                    self.enable_buttons()



                    messagebox.showerror(

                        "Sequential Error",

                        message[1]

                    )



                # ------------------------------------------

                # PARALLEL COMPLETE

                # ------------------------------------------



                elif message_type == "parallel_done":



                    pages = message[1]

                    execution_time = message[2]

                    workers = message[3]



                    self.update_parallel(

                        pages,

                        execution_time,

                        workers

                    )



                    self.enable_buttons()



                # ------------------------------------------

                # PARALLEL ERROR

                # ------------------------------------------



                elif message_type == "parallel_error":



                    self.enable_buttons()



                    messagebox.showerror(

                        "Parallel Error",

                        message[1]

                    )



        except queue.Empty:



            pass



        # Run again in main Tkinter thread



        self.root.after(

            100,

            self.process_queue

        )



    # ======================================================

    # INPUTS

    # ======================================================



    def get_inputs(self):



        url = self.url_entry.get().strip()



        try:



            pages = int(

                self.pages_entry.get()

            )



            workers = int(

                self.workers_combo.get()

            )



        except ValueError:



            messagebox.showerror(

                "Invalid Input",

                "Enter valid numbers."

            )



            return None



        if not url:



            messagebox.showerror(

                "Invalid URL",

                "Enter a starting URL."

            )



            return None



        if pages <= 0:



            messagebox.showerror(

                "Invalid Pages",

                "Number of pages must be greater than 0."

            )



            return None



        return url, pages, workers



    # ======================================================

    # GENERATE TEST PAGES

    # ======================================================



    def generate_test_pages(self):



        try:



            pages = int(

                self.pages_entry.get()

            )



        except ValueError:



            messagebox.showerror(

                "Invalid Pages",

                "Enter a valid number."

            )



            return



        if pages <= 0:



            messagebox.showerror(

                "Invalid Pages",

                "Number of pages must be greater than 0."

            )



            return



        self.disable_buttons()



        self.status_label.config(

            text=f"Generating {pages} test pages..."

        )



        thread = threading.Thread(

            target=self.generate_pages_task,

            args=(pages,),

            daemon=True

        )



        thread.start()



    def generate_pages_task(

        self,

        pages

    ):



        try:



            generate_pages(

                pages

            )



            self.result_queue.put(

                (

                    "generate_done",

                    pages

                )

            )



        except Exception as e:



            self.result_queue.put(

                (

                    "generate_error",

                    str(e)

                )

            )



    # ======================================================

    # RUN SEQUENTIAL

    # ======================================================



    def run_sequential(self):



        inputs = self.get_inputs()



        if inputs is None:

            return



        url, pages, workers = inputs



        self.disable_buttons()



        self.status_label.config(

            text=f"Running sequential crawler for {pages} pages..."

        )



        thread = threading.Thread(

            target=self.sequential_task,

            args=(url, pages),

            daemon=True

        )



        thread.start()



    def sequential_task(

        self,

        url,

        pages

    ):



        try:



            execution_time = crawl_sequential(

                start_url=url,

                max_pages=pages,

                verbose=False

            )



            try:



                df = pd.read_csv(

                    "results/sequential_results.csv"

                )



                crawled_pages = len(df)



            except Exception:



                crawled_pages = 0



            self.result_queue.put(

                (

                    "sequential_done",

                    crawled_pages,

                    execution_time

                )

            )



        except Exception as e:



            self.result_queue.put(

                (

                    "sequential_error",

                    str(e)

                )

            )



    # ======================================================

    # UPDATE SEQUENTIAL

    # ======================================================



    def update_sequential(

        self,

        pages,

        execution_time

    ):



        self.sequential_pages = pages
        self.sequential_time = execution_time

        if self.parallel_pages != pages:
            self.parallel_time = None
            self.parallel_pages = None
            self.parallel_workers = None
        self.current_pages = pages



        self.seq_pages_label.config(

            text=str(pages)

        )



        self.seq_time_label.config(

            text=f"{execution_time:.3f} s"

        )



        self.status_label.config(

            text="Sequential crawling completed."

        )



        self.calculate_current_metrics()



    # ======================================================

    # RUN PARALLEL

    # ======================================================



    def run_parallel(self):



        inputs = self.get_inputs()



        if inputs is None:

            return



        url, pages, workers = inputs



        self.disable_buttons()



        self.status_label.config(

            text=f"Running parallel crawler with {workers} workers..."

        )



        thread = threading.Thread(

            target=self.parallel_task,

            args=(url, pages, workers),

            daemon=True

        )



        thread.start()



    def parallel_task(

        self,

        url,

        pages,

        workers

    ):



        try:



            execution_time = crawl_parallel(

                start_url=url,

                max_pages=pages,

                workers=workers,

                verbose=False

            )



            try:



                df = pd.read_csv(

                    "results/parallel_results.csv"

                )



                crawled_pages = len(df)



            except Exception:



                crawled_pages = 0



            self.result_queue.put(

                (

                    "parallel_done",

                    crawled_pages,

                    execution_time,

                    workers

                )

            )



        except Exception as e:



            self.result_queue.put(

                (

                    "parallel_error",

                    str(e)

                )

            )



    # ======================================================

    # UPDATE PARALLEL

    # ======================================================



    def update_parallel(

        self,

        pages,

        execution_time,

        workers

    ):



        self.parallel_pages = pages
        self.parallel_time = execution_time
        self.parallel_workers = workers
        self.current_pages = pages

        if self.sequential_pages != pages:
            self.sequential_time = None



        self.par_pages_label.config(

            text=str(pages)

        )



        self.par_time_label.config(

            text=f"{execution_time:.3f} s"

        )



        self.par_workers_label.config(

            text=str(workers)

        )



        self.status_label.config(

            text="Parallel crawling completed."

        )



        self.calculate_current_metrics()



    # ======================================================

    # CALCULATE PERFORMANCE

    # ======================================================



    def calculate_current_metrics(self):



        if self.sequential_time is None:

            return



        if self.parallel_time is None:

            return



        if self.parallel_workers is None:

            return



        if self.parallel_time <= 0:

            return



        speedup = (

            self.sequential_time /

            self.parallel_time

        )



        efficiency = (

            speedup /

            self.parallel_workers

        ) * 100



        self.speedup_label.config(

            text=f"{speedup:.3f}x"

        )



        self.efficiency_label.config(

            text=f"{efficiency:.2f}%"

        )



        # Save experiment



        self.save_gui_result(

            self.current_pages,

            self.parallel_workers,

            self.sequential_time,

            self.parallel_time,

            speedup,

            efficiency

        )



        # Update table



        self.load_gui_results()



        # Generate graphs



        self.generate_dynamic_graphs()



    # ======================================================

    # SAVE RESULT

    # ======================================================



    def save_gui_result(

        self,

        pages,

        workers,

        sequential_time,

        parallel_time,

        speedup,

        efficiency

    ):



        os.makedirs(

            "results",

            exist_ok=True

        )



        new_data = pd.DataFrame(

            [{

                "pages": pages,

                "workers": workers,

                "sequential_time": round(

                    sequential_time,

                    3

                ),

                "parallel_time": round(

                    parallel_time,

                    3

                ),

                "speedup": round(

                    speedup,

                    3

                ),

                "efficiency": round(

                    efficiency,

                    2

                )

            }]

        )



        if os.path.exists(

            GUI_RESULTS_FILE

        ):



            old_data = pd.read_csv(

                GUI_RESULTS_FILE

            )



            old_data = old_data[

                ~(

                    (old_data["pages"] == pages)

                    &

                    (old_data["workers"] == workers)

                )

            ]



            final_data = pd.concat(

                [

                    old_data,

                    new_data

                ],

                ignore_index=True

            )



        else:



            final_data = new_data



        final_data.to_csv(

            GUI_RESULTS_FILE,

            index=False

        )



    # ======================================================

    # LOAD TABLE

    # ======================================================



    def load_gui_results(self):



        for item in self.table.get_children():



            self.table.delete(

                item

            )



        if not os.path.exists(

            GUI_RESULTS_FILE

        ):



            return



        try:



            df = pd.read_csv(

                GUI_RESULTS_FILE

            )



            df = df.sort_values(

                [

                    "pages",

                    "workers"

                ]

            )



            for _, row in df.iterrows():



                self.table.insert(

                    "",

                    "end",

                    values=(

                        int(row["pages"]),

                        "Sequential + Parallel",

                        int(row["workers"]),

                        f"{row['sequential_time']:.3f}",

                        f"{row['parallel_time']:.3f}",

                        f"{row['speedup']:.3f}x",

                        f"{row['efficiency']:.2f}%"

                    )

                )



        except Exception as e:



            print(

                "Table loading error:",

                e

            )



    # ======================================================

    # CLEAR CURRENT

    # ======================================================



    def clear_current(self):



        self.sequential_time = None
        self.sequential_pages = None
        self.parallel_time = None
        self.parallel_pages = None
        self.parallel_workers = None
        self.current_pages = None



        self.seq_pages_label.config(

            text="-"

        )



        self.seq_time_label.config(

            text="-"

        )



        self.par_pages_label.config(

            text="-"

        )



        self.par_time_label.config(

            text="-"

        )



        self.par_workers_label.config(

            text="-"

        )



        self.speedup_label.config(

            text="-"

        )



        self.efficiency_label.config(

            text="-"

        )



        self.status_label.config(

            text="Current results cleared."

        )



    # ======================================================

    # BUTTON CONTROL

    # ======================================================



    def disable_buttons(self):



        self.generate_button.config(

            state="disabled"

        )



        self.sequential_button.config(

            state="disabled"

        )



        self.parallel_button.config(

            state="disabled"

        )



        self.clear_button.config(

            state="disabled"

        )



    def enable_buttons(self):



        self.generate_button.config(

            state="normal"

        )



        self.sequential_button.config(

            state="normal"

        )



        self.parallel_button.config(

            state="normal"

        )



        self.clear_button.config(

            state="normal"

        )





# ==========================================================

# START APPLICATION

# ==========================================================



if __name__ == "__main__":



    root = tk.Tk()



    app = CrawlerGUI(

        root

    )



    root.mainloop()